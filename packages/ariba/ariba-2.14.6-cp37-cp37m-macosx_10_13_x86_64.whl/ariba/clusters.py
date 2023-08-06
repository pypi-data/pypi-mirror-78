import signal
import time
import os
import copy
import json
import tempfile
import pickle
import itertools
import sys
import multiprocessing
import pyfastaq
import minimap_ariba
from ariba import cluster, common, histogram, mlst_reporter, read_store, report, report_filter, reference_data, tb

class Error (Exception): pass

# passing shared objects (remaining_clusters) through here and thus making them
# explicit arguments to Pool.startmap when running this function. That seems to be
# a recommended safe transfer mechanism as opposed making them attributes of a
# pre-constructed 'obj' variable (although the docs are a bit hazy on that)
def _run_cluster(obj, verbose, clean, fails_dir, remaining_clusters, remaining_clusters_lock):
    failed_clusters = os.listdir(fails_dir)

    if len(failed_clusters) > 0:
        print('Other clusters failed. Will not start cluster', obj.name, file=sys.stderr)
        return obj

    if verbose:
        print('Start running cluster', obj.name, 'in directory', obj.root_dir, flush=True)
    try:
        obj.run(remaining_clusters=remaining_clusters,remaining_clusters_lock=remaining_clusters_lock)
    except:
        print('Failed cluster:', obj.name, file=sys.stderr)
        with open(os.path.join(fails_dir, obj.name), 'w'):
            pass

    if verbose:
        print('Finished running cluster', obj.name, 'in directory', obj.root_dir, flush=True)

    if clean:
        if verbose:
            print('Deleting cluster dir', obj.root_dir, flush=True)
        if os.path.exists(obj.root_dir):
            try:
                common.rmtree(obj.root_dir)
            except:
                pass

    return obj


class Clusters:
    def __init__(self,
      refdata_dir,
      reads_1,
      reads_2,
      outdir,
      extern_progs,
      version_report_lines=None,
      assembly_kmer=21,
      assembly_coverage=100,
      threads=1,
      verbose=False,
      assembler='fermilite',
      spades_mode='rna',
      spades_options=None,
      max_insert=1000,
      min_scaff_depth=10,
      nucmer_min_id=90,
      nucmer_min_len=20,
      nucmer_breaklen=200,
      assembled_threshold=0.95,
      unique_threshold=0.03,
      max_gene_nt_extend=30,
      clean=True,
      tmp_dir=None,
    ):
        self.refdata_dir = os.path.abspath(refdata_dir)
        self.refdata, self.cluster_ids = self._load_reference_data_from_dir(refdata_dir)
        self.reads_1 = os.path.abspath(reads_1)
        self.reads_2 = os.path.abspath(reads_2)
        self.outdir = os.path.abspath(outdir)
        self.extern_progs = extern_progs
        self.clusters_tsv = os.path.abspath(os.path.join(refdata_dir, '02.cdhit.clusters.tsv'))
        self.all_ref_seqs_fasta = os.path.abspath(os.path.join(refdata_dir, '02.cdhit.all.fa'))

        if version_report_lines is None:
            self.version_report_lines = []
        else:
            self.version_report_lines = version_report_lines

        self.clean = clean
        self.logs_dir = os.path.join(self.outdir, 'Logs')

        self.assembler = assembler
        self.assembly_kmer = assembly_kmer
        self.assembly_coverage = assembly_coverage
        self.spades_mode = spades_mode
        self.spades_options = spades_options

        self.cdhit_files_prefix = os.path.join(self.refdata_dir, 'cdhit')
        self.cdhit_cluster_representatives_fa = self.cdhit_files_prefix + '.cluster_representatives.fa'
        self.bam_prefix = os.path.join(self.outdir, 'map_reads_to_cluster_reps')
        self.bam = self.bam_prefix + '.bam'
        self.report_file_all_tsv = os.path.join(self.outdir, 'debug.report.tsv')
        self.report_file_filtered = os.path.join(self.outdir, 'report.tsv')
        self.mlst_reports_prefix = os.path.join(self.outdir, 'mlst_report')
        self.mlst_profile_file = os.path.join(self.refdata_dir, 'pubmlst.profile.txt')
        self.tb_resistance_calls_file = os.path.join(self.outdir, 'tb.resistance.json')
        self.catted_assembled_seqs_fasta = os.path.join(self.outdir, 'assembled_seqs.fa.gz')
        self.catted_genes_matching_refs_fasta = os.path.join(self.outdir, 'assembled_genes.fa.gz')
        self.catted_assemblies_fasta = os.path.join(self.outdir, 'assemblies.fa.gz')
        self.threads = threads
        self.verbose = verbose

        self.max_insert = max_insert

        self.insert_hist_bin = 10
        self.insert_hist = histogram.Histogram(self.insert_hist_bin)
        self.insert_size = None
        self.insert_sspace_sd = None
        self.insert_proper_pair_max = None

        self.min_scaff_depth = min_scaff_depth
        self.nucmer_min_id = nucmer_min_id
        self.nucmer_min_len = nucmer_min_len
        self.nucmer_breaklen = nucmer_breaklen

        self.assembled_threshold = assembled_threshold
        self.unique_threshold = unique_threshold
        self.max_gene_nt_extend = max_gene_nt_extend

        self.cluster_to_dir = {}  # gene name -> abs path of cluster directory
        self.clusters = {}        # gene name -> Cluster object
        self.cluster_read_counts = {} # gene name -> number of reads
        self.cluster_base_counts = {} # gene name -> number of bases
        self.pool = None
        self.fails_dir = os.path.join(self.outdir ,'.fails')
        self.clusters_all_ran_ok = True

        for d in [self.outdir, self.logs_dir, self.fails_dir]:
            try:
                os.mkdir(d)
            except:
                raise Error('Error mkdir ' + d)
        if tmp_dir is None:
            if 'ARIBA_TMPDIR' in os.environ:
                tmp_dir = os.path.abspath(os.environ['ARIBA_TMPDIR'])
            elif 'TMPDIR' in os.environ:
                tmp_dir = os.path.abspath(os.environ['TMPDIR'])
            else:
                tmp_dir = self.outdir

        if not os.path.exists(tmp_dir):
            raise Error('Temporary directory ' + tmp_dir + ' not found. Cannot continue')

        if self.clean:
            self.tmp_dir_obj = tempfile.TemporaryDirectory(prefix='ariba.tmp.', dir=os.path.abspath(tmp_dir))
            self.tmp_dir = self.tmp_dir_obj.name
        else:
            self.tmp_dir_obj = None
            self.tmp_dir = os.path.join(self.outdir, 'clusters')
            try:
                os.mkdir(self.tmp_dir)
            except:
                raise Error('Error making directory ' + self.tmp_dir)

        if self.verbose:
            print('Temporary directory:', self.tmp_dir)

        for i in [x for x in dir(signal) if x.startswith("SIG") and x not in {'SIGCHLD', 'SIGCLD', 'SIGPIPE', 'SIGTSTP', 'SIGCONT'}]:
            try:
                signum = getattr(signal, i)
                signal.signal(signum, self._receive_signal)
            except:
                pass


    def _stop_pool(self):
        if self.pool is None:
            return
        self.pool.close()
        self.pool.terminate()
        while len(multiprocessing.active_children()) > 0:
            time.sleep(1)


    def _emergency_stop(self):
        self._stop_pool()
        if self.clean:
            try:
                self.tmp_dir_obj.cleanup()
            except:
                pass


    def _receive_signal(self, signum, stack):
        print('Stopping! Signal received:', signum, file=sys.stderr, flush=True)
        self._emergency_stop()
        sys.exit(1)


    @classmethod
    def _load_reference_data_info_file(cls, filename):
        data = {
            'genetic_code': None
        }

        with open(filename) as f:
            for line in f:
                key, val = line.rstrip().split('\t')
                if key in data:
                    data[key] = val

        if None in data.values():
            missing_values = [x for x in data if data[x] is None]
            raise Error('Error reading reference info file ' + filename + '. These values not found: ' + ','.join(missing_values))

        data['genetic_code'] = int(data['genetic_code'])
        return data


    @staticmethod
    def _load_reference_data_from_dir(indir):
        if not os.path.exists(indir):
            raise Error('Error loading reference data. Input directory ' + indir + ' not found. Cannot continue')

        fasta_file = os.path.join(indir, '02.cdhit.all.fa')
        metadata_file = os.path.join(indir, '01.filter.check_metadata.tsv')
        info_file = os.path.join(indir, '00.info.txt')
        parameters_file = os.path.join(indir, '00.params.json')
        clusters_pickle_file = os.path.join(indir, '02.cdhit.clusters.pickle')
        params = Clusters._load_reference_data_info_file(info_file)
        refdata = reference_data.ReferenceData(
            [fasta_file],
            [metadata_file],
            genetic_code=params['genetic_code'],
            parameters_file=parameters_file,
        )

        with open(clusters_pickle_file, 'rb') as f:
            cluster_ids = pickle.load(f)

        return refdata, cluster_ids


    def _map_and_cluster_reads(self):
        if self.verbose:
            print('{:_^79}'.format(' Mapping reads to clustered genes '), flush=True)

        minimap_prefix = 'minimap'

        self._minimap_reads_to_all_ref_seqs(
            self.clusters_tsv,
            self.all_ref_seqs_fasta,
            self.reads_1,
            self.reads_2,
            minimap_prefix,
            verbose=self.verbose
        )

        if self.verbose:
            print('Finished mapping\n')
            print('{:_^79}'.format(' Generating clusters '), flush=True)

        self.cluster_to_rep, self.cluster_read_counts, self.cluster_base_counts, self.insert_hist, self.proper_pairs = self._load_minimap_files(minimap_prefix, self.insert_hist_bin)
        self.cluster_to_dir = {x: os.path.join(self.tmp_dir, x) for x in self.cluster_to_rep}
        reads_file_for_read_store = minimap_prefix + '.reads'

        if len(self.cluster_read_counts):
            if self.verbose:
                filehandle = sys.stdout
            else:
                filehandle = None

            self.read_store = read_store.ReadStore(
              reads_file_for_read_store,
              os.path.join(self.outdir, 'read_store'),
              log_fh=filehandle
            )

        os.unlink(reads_file_for_read_store)

        if self.clean:
            for suffix in ['cluster2representative', 'clusterCounts', 'insertHistogram', 'properPairs']:
                filename = minimap_prefix + '.' + suffix
                try:
                    os.unlink(filename)
                except:
                    pass

        if self.verbose:
            print('Found', self.proper_pairs, 'proper read pairs from minimap')
            print('Total clusters to perform local assemblies:', len(self.cluster_to_dir), flush=True)


    @staticmethod
    def _minimap_reads_to_all_ref_seqs(clusters_tsv, ref_fasta, reads_1, reads_2, outprefix, verbose=False):
        got = minimap_ariba.minimap_ariba(clusters_tsv, ref_fasta, reads_1, reads_2, outprefix)
        if (got != 0):
            raise Error('Error running minimap. Cannot continue')


    @classmethod
    def _load_minimap_out_cluster2representative(cls, infile):
        cluster2rep = {}

        with open(infile) as f:
            for line in f:
                cluster, rep = line.rstrip().split('\t')
                cluster2rep[cluster] = rep

        return cluster2rep


    @classmethod
    def _load_minimap_out_cluster_counts(cls, infile):
        reads = {}
        bases = {}

        with open(infile) as f:
            for line in f:
                cluster, read, base = line.rstrip().split('\t')
                reads[cluster] = int(read)
                bases[cluster] = int(base)

        return reads, bases


    @classmethod
    def _load_minimap_insert_histogram(cls, infile, bin_size):
        hist = histogram.Histogram(bin_size)

        with open(infile) as f:
            for line in f:
                value, count = line.rstrip().split('\t')
                hist.add(int(value), count=int(count))

        return hist


    @classmethod
    def _load_minimap_proper_pairs(cls, infile):
        with open(infile) as f:
            for line in f:
                pairs = int(line.rstrip())
                break

        return pairs


    @staticmethod
    def _load_minimap_files(inprefix, hist_bin_size):
        cluster2rep = Clusters._load_minimap_out_cluster2representative(inprefix + '.cluster2representative')
        cluster_read_count, cluster_base_count = Clusters._load_minimap_out_cluster_counts(inprefix + '.clusterCounts')
        insert_hist = Clusters._load_minimap_insert_histogram(inprefix + '.insertHistogram', hist_bin_size)
        proper_pairs = Clusters._load_minimap_proper_pairs(inprefix + '.properPairs')
        return cluster2rep, cluster_read_count, cluster_base_count, insert_hist, proper_pairs


    def _set_insert_size_data(self):
        if len(self.insert_hist) == 0:
            return False
        else:
            (x, self.insert_size, pc95, self.insert_sspace_sd) = self.insert_hist.stats()
            self.insert_sspace_sd = min(1, self.insert_sspace_sd)
            self.insert_proper_pair_max = 1.1 * pc95
            if self.verbose:
                print('\nInsert size information from reads mapped to reference genes:')
                print('Insert size:', self.insert_size, sep='\t')
                print('Insert sspace sd:', self.insert_sspace_sd, sep='\t')
                print('Max insert:', self.insert_proper_pair_max, sep='\t')
                print()
            return True


    def _init_and_run_clusters(self):
        if len(self.cluster_to_dir) == 0:
            raise Error('Did not get any reads mapped to genes. Cannot continue')

        counter = 0
        cluster_list = []
        self.log_files = []

        # How the thread count withing each Cluster.run is managed:
        # We want to handle those cases where there are more total threads allocated to the application than there are clusters
        # remaining to run (for example,
        # there are only two references, and eight threads). If we keep the default thread value of 1 in cluster. Cluster,
        # then we will be wasting the allocated threads. The most simple approach would be to divide all threads equally between clusters
        # before calling Pool.map. Multithreaded external programs like Spades and Bowtie2 are then called with multiple threads. That should
        # never be slower than keeping just one thread in cluster.Cluster, except maybe in the extreme cases when (if)
        # a multi-threaded run of the external program takes longer wall-clock time than a single-threaded one.
        # However, this solution would always keep
        # Cluster.threads=1 if the initial number of clusters > number of total threads. This can result in inefficiency at the
        # tail of the Pool.map execution flow - when the clusters are getting finished overall, we are waiting for the completion of
        # fewer and fewer remaining
        # single-threaded cluster tasks while more and more total threads are staying idle. We mitigate this through the following approach:
        # - Create a shared Value object that holds the number of remaining clusters (remaining_clusters).
        # - Each Cluster.run decrements the remaining_clusters when it completes
        # - Cluster.run sets its own thread count to max(1,threads_total//remaining_clusters). This can be done as many times
        #   as needed at various points within Cluster.run (e.g. once before Spades is called, and again before Bowtie2 is called),
        #   in order to catch more idle threads.
        # This is a simple and conservative approach to adaptively use all threads at the tail of the map flow. It
        # never over-subscribes the threads, and it does not require any extra blocking within Cluster.run in order to
        # wait for threads becoming available.

        for cluster_name in sorted(self.cluster_to_dir):
            counter += 1

            if self.cluster_read_counts[cluster_name] <= 2:
                if self.verbose:
                    print('Not constructing cluster ', cluster_name, ' because it only has ', self.cluster_read_counts[cluster_name], ' reads (', counter, ' of ', len(self.cluster_to_dir), ')', sep='')
                continue

            if self.verbose:
                print('Constructing cluster ', cluster_name, ' (', counter, ' of ', len(self.cluster_to_dir), ')', sep='')
            new_dir = self.cluster_to_dir[cluster_name]
            self.log_files.append(os.path.join(self.logs_dir, cluster_name + '.log'))

            cluster_list.append(cluster.Cluster(
                new_dir,
                cluster_name,
                self.refdata,
                all_ref_seqs_fasta=self.all_ref_seqs_fasta,
                fail_file=os.path.join(self.fails_dir, cluster_name),
                read_store=self.read_store,
                reference_names=self.cluster_ids[cluster_name],
                logfile=self.log_files[-1],
                assembly_coverage=self.assembly_coverage,
                assembly_kmer=self.assembly_kmer,
                assembler=self.assembler,
                max_insert=self.insert_proper_pair_max,
                min_scaff_depth=self.min_scaff_depth,
                nucmer_min_id=self.nucmer_min_id,
                nucmer_min_len=self.nucmer_min_len,
                nucmer_breaklen=self.nucmer_breaklen,
                reads_insert=self.insert_size,
                sspace_k=self.min_scaff_depth,
                sspace_sd=self.insert_sspace_sd,
                threads=1, # initially set to 1, then will adaptively self-modify while running
                assembled_threshold=self.assembled_threshold,
                unique_threshold=self.unique_threshold,
                max_gene_nt_extend=self.max_gene_nt_extend,
                spades_mode=self.spades_mode,
                spades_options=self.spades_options,
                clean=self.clean,
                extern_progs=self.extern_progs,
                threads_total=self.threads
            ))
        # Here is why we use proxy objects from a Manager process below
        # instead of simple shared multiprocessing.Value counter:
        # Shared memory objects in multiprocessing use tempfile module to
        # create temporary directory, then create temporary file inside it,
        # memmap the file and unlink it. If TMPDIR envar points to a NFS
        # mount, the final cleanup handler from multiprocessing will often
        # return an exception due to a stale NFS file (.nfsxxxx) from a shutil.rmtree
        # call. See help on tempfile.gettempdir() for how the default location of
        # temporary files is selected. The exception is caught in except clause
        # inside multiprocessing cleanup, and only a harmless traceback is printed,
        # but it looks very spooky to the user and causes confusion. We use
        # instead shared proxies from the Manager. Those do not rely on shared
        # memory, and thus bypass the NFS issues. The counter is accesses infrequently
        # relative to computations, so the performance does not suffer.
        # default authkey in the manager will be some generated random-looking string
        manager = multiprocessing.Manager()
        remaining_clusters = manager.Value('l',len(cluster_list))
        # manager.Value does not provide access to the internal RLock that we need for
        # implementing atomic -=, so we need to carry around a separate RLock object.
        remaining_clusters_lock = manager.RLock()
        try:
            if self.threads > 1:
                self.pool = multiprocessing.Pool(self.threads)
                cluster_list = self.pool.starmap(_run_cluster, zip(cluster_list, itertools.repeat(self.verbose), itertools.repeat(self.clean), itertools.repeat(self.fails_dir),
                                                                   itertools.repeat(remaining_clusters),itertools.repeat(remaining_clusters_lock)))
                # harvest the pool as soon as we no longer need it
                self.pool.close()
                self.pool.join()
            else:
                for c in cluster_list:
                    _run_cluster(c, self.verbose, self.clean, self.fails_dir, remaining_clusters, remaining_clusters_lock)
        except:
            self.clusters_all_ran_ok = False

        if self.verbose:
            print('Final value of remaining_clusters counter:', remaining_clusters)
        remaining_clusters = None
        remaining_clusters_lock = None
        manager.shutdown()

        if len(os.listdir(self.fails_dir)) > 0:
            self.clusters_all_ran_ok = False

        self.clusters = {c.name: c for c in cluster_list}


    @staticmethod
    def _write_report(clusters_in, tsv_out):
        columns = copy.copy(report.columns)
        columns[0] = '#' + columns[0]

        f = pyfastaq.utils.open_file_write(tsv_out)
        print('\t'.join(columns), file=f)
        columns[0] = columns[0][1:]

        for seq_name in sorted(clusters_in):
            if clusters_in[seq_name].report_lines is None:
                continue

            for line in clusters_in[seq_name].report_lines:
                print(line, file=f)

        pyfastaq.utils.close(f)


    def _write_catted_assemblies_fasta(self, outfile):
        f = pyfastaq.utils.open_file_write(outfile)

        for gene in sorted(self.clusters):
            try:
                seq_dict = self.clusters[gene].assembly.sequences
            except:
                continue

            for seq_name in sorted(seq_dict):
                print(seq_dict[seq_name], file=f)

        pyfastaq.utils.close(f)


    def _write_catted_assembled_seqs_fasta(self, outfile):
        f = pyfastaq.utils.open_file_write(outfile)

        for gene in sorted(self.clusters):
            try:
                seq_dict = self.clusters[gene].assembly_compare.assembled_reference_sequences
            except:
                continue

            for seq_name in sorted(seq_dict):
                print(seq_dict[seq_name], file=f)

        pyfastaq.utils.close(f)


    def _write_catted_genes_matching_refs_fasta(self, outfile):
        f = pyfastaq.utils.open_file_write(outfile)

        for gene in sorted(self.clusters):
            if self.clusters[gene].assembly_compare is not None and self.clusters[gene].assembly_compare.gene_matching_ref is not None:
                seq = copy.copy(self.clusters[gene].assembly_compare.gene_matching_ref)
                seq.id += '.' + '.'.join([
                    self.clusters[gene].assembly_compare.gene_matching_ref_type,
                    str(self.clusters[gene].assembly_compare.gene_start_bases_added),
                    str(self.clusters[gene].assembly_compare.gene_end_bases_added)
                ])
                print(seq, file=f)

        pyfastaq.utils.close(f)


    def _clean(self):
        if self.clean:
            common.rmtree(self.fails_dir)

            try:
                self.tmp_dir_obj.cleanup()
            except:
                pass

            if self.verbose:
                print('Deleting Logs directory', self.logs_dir)
            common.rmtree(self.logs_dir)

            try:
                if self.verbose:
                    print('Deleting reads store files', self.read_store.outfile + '[.tbi]')
                self.read_store.clean()
            except:
                pass
        else:
            if self.verbose:
                print('Not deleting anything because --noclean used')


    @classmethod
    def _write_mlst_reports(cls, mlst_profile_file, ariba_report_tsv, outprefix, verbose=False):
        if os.path.exists(mlst_profile_file):
            if verbose:
                print('\nMaking MLST reports', flush=True)
            reporter = mlst_reporter.MlstReporter(ariba_report_tsv, mlst_profile_file, outprefix)
            reporter.run()


    @classmethod
    def _write_tb_resistance_calls_json(cls, ariba_report_tsv, outfile):
        calls = tb.report_to_resistance_dict(ariba_report_tsv)
        with open(outfile, 'w') as f:
            json.dump(calls, f, sort_keys=True, indent=4)


    def write_versions_file(self, original_dir):
        with open('version_info.txt', 'w') as f:
            print('ARIBA run with this command:', file=f)
            print(' '.join([sys.argv[0]] + sys.argv[1:]), file=f)
            print('from this directory:', original_dir, file=f)
            print(file=f)
            print(*self.version_report_lines, sep='\n', file=f)


    def run(self):
        try:
            self._run()
        except Error as err:
            self._emergency_stop()
            raise Error('Something went wrong during ariba run. Cannot continue. Error was:\n' + str(err))


    def _run(self):
        cwd = os.getcwd()
        try:
            os.chdir(self.outdir)
            self.write_versions_file(cwd)
            self._map_and_cluster_reads()
            self.log_files = None

            if len(self.cluster_to_dir) > 0:
                got_insert_data_ok = self._set_insert_size_data()
                if not got_insert_data_ok:
                    print('WARNING: not enough proper read pairs (found ' + str(self.proper_pairs) + ') to determine insert size.', file=sys.stderr)
                    print('This probably means that very few reads were mapped at all. No local assemblies will be run', file=sys.stderr)
                    if self.verbose:
                        print('Not enough proper read pairs mapped to determine insert size. Skipping all assemblies.', flush=True)
                else:
                    if self.verbose:
                        print('{:_^79}'.format(' Assembling each cluster '))
                        print('Will run', self.threads, 'cluster(s) in parallel', flush=True)
                    self._init_and_run_clusters()
                    if self.verbose:
                        print('Finished assembling clusters\n')
            else:
                if self.verbose:
                    print('No reads mapped. Skipping all assemblies', flush=True)
                print('WARNING: no reads mapped to reference genes. Therefore no local assemblies will be run', file=sys.stderr)

            if not self.clusters_all_ran_ok:
                raise Error('At least one cluster failed! Stopping...')

            if self.verbose:
                print('{:_^79}'.format(' Writing reports '), flush=True)
                print('Making', self.report_file_all_tsv)
            self._write_report(self.clusters, self.report_file_all_tsv)

            if self.verbose:
                print('Making', self.report_file_filtered)
            rf = report_filter.ReportFilter(infile=self.report_file_all_tsv)
            rf.run(self.report_file_filtered)

            if self.verbose:
                print()
                print('{:_^79}'.format(' Writing fasta of assembled sequences '), flush=True)
                print(self.catted_assembled_seqs_fasta, 'and', self.catted_genes_matching_refs_fasta, flush=True)
            self._write_catted_assembled_seqs_fasta(self.catted_assembled_seqs_fasta)
            self._write_catted_genes_matching_refs_fasta(self.catted_genes_matching_refs_fasta)
            self._write_catted_assemblies_fasta(self.catted_assemblies_fasta)

            if self.log_files is not None:
                clusters_log_file = os.path.join(self.outdir, 'log.clusters.gz')
                if self.verbose:
                    print()
                    print('{:_^79}'.format(' Catting cluster log files '), flush=True)
                    print('Writing file', clusters_log_file, flush=True)
                common.cat_files(self.log_files, clusters_log_file)

            if self.verbose:
                print()
                print('{:_^79}'.format(' Cleaning files '), flush=True)
            self._clean()

            Clusters._write_mlst_reports(self.mlst_profile_file, self.report_file_filtered, self.mlst_reports_prefix, verbose=self.verbose)

            if 'tb' in self.refdata.extra_parameters and self.refdata.extra_parameters['tb']:
                Clusters._write_tb_resistance_calls_json(self.report_file_filtered, self.tb_resistance_calls_file)

            if self.clusters_all_ran_ok and self.verbose:
                print('\nAll done!\n')
        finally:
            os.chdir(cwd)
