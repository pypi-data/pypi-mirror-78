# HaMiP: DNA hydroxymethylation analysis of Cytosine-5-methylenesulfonate ImmunoPrecipitation sequencing

A scalable, accurate, and efficient solution for hydroxymethylation analysis of CMS-IP sequencing data.

![Workflow of HaMiP.](https://github.com/lijinbio/HaMiP/raw/master/HaMiP_flowchart.png)

## Installation

HaMiP has been deployed in Bioconda at https://anaconda.org/bioconda/HaMiP. It is encouraged to install HaMiP from Bioconda due to most runtime dependencies will be installed automatically. The following channels should be added in Conda. Namely,

```
conda config --add channels defaults
conda config --add channels bioconda
conda config --add channels conda-forge
conda install HaMiP
```

Alternatively, HaMiP has been also deployed in PyPI at https://pypi.org/project/HaMiP, and it can be installed via `pip`.

```
pip3 install HaMiP
```

In some cases, users want to build HaMiP manually from source code at https://github.com/lijinbio/HaMiP. Below is an example installation steps.

```
git clone https://github.com/lijinbio/HaMiP.git
cd HaMiP
python3 setup.py install
```

In order to run HaMiP after a manual installation, the following dependent software are required.

| Software | URL |
|-------|-------|
| Python 3 | https://www.python.org |
| Matplotlib | https://matplotlib.org |
| PyYAML | https://pyyaml.org |
| bedtools | https://bedtools.readthedocs.io |
| fetchChromSizes | http://hgdownload.cse.ucsc.edu/admin/exe/ |
| R software | https://www.r-project.org |
| R package DESeq2 | https://bioconductor.org/packages/release/bioc/html/DESeq2.html |
| R package genefilter | https://bioconductor.org/packages/release/bioc/html/genefilter.html |
| R package DescTools | https://cran.r-project.org/web/packages/DescTools/index.html |
| Gawk | https://www.gnu.org/software/gawk |
| MOABS | https://github.com/sunnyisgalaxy/moabs |

## Documentation

HaMiP takes in a configuration file for input data and program parameters. HaMiP can be run end-to-end, starting from raw FASTQ files to peak calling and differential hydroxymethylation identification. One can also start the pipeline from intermediate steps. For example, using alignment files as input so that mapping steps will be skipped.

### Inspection of configuration

The configuration file is in a YAML format. Two example templates are `config_fastq.yaml` and `config_bam.yaml` under https://github.com/lijinbio/HaMiP/blob/master/config. `config_fastq.yaml` is used as a full HaMiP running from FASTQ inputs, while `config_bam.yaml` is adapted to input existing BAM files so that HaMiP will skip the long-time alignment step. The inspection of configuration is explained below.

1. sampleinfo

The sampleinfo section defines metadata information in analysis. Below metadata information can be specified.

| Parameter | Description |
|-------|-------|
| sampleinfo.sampleid | the unique identifier to one sample |
| sampleinfo.group | the biological group of the sample, e.g., KO or WT |
| sampleinfo.filenames | the absolute path of raw FASTQ files |
| sampleinfo.reference | the absolute path of the reference BAM file when `aligninfo.inputbam` is True |
| sampleinfo.spikein | the absolute path of the spike-in BAM file when `aligninfo.inputbam` and `aligninfo.usespikein` are True |

 2. groupinfo

This section defines biological comparison `group1` - `group2`, e.g., KO - WT.

| Parameter | Description |
|-------|-------|
| groupinfo.group1 | the first group in biological comparison |
| groupinfo.group2 | the second group in biological comparison |

3. resultdir

This directory is default working directory storing intemediate result files, such as BAM and BED files.

4. aligninfo

This section specifies parameters used in raw reads alignment.

| Parameter | Description |
|-------|-------|
| aligninfo.inputbam | True for BAM inputs. Default: FASTQ inputs. |
| aligninfo.reference | FASTA file of the reference genome, e.g. `hg38.fa`. |
| aligninfo.usespikein | True for spike-in libraries, otherwise False. This option controls the normalization method, either a spike-in normalization using spike-in mapping, or reduced to WIG sum in the reference genome. |
| aligninfo.spikein | FASTA file of the spike-in genome, e.g. `mm10.fa`. |
| aligninfo.statfile | the output statistics file. This file includes quality control statistics as well as estimated normalization factors. |
| aligninfo.barplotinfo | a barplot of normalized WIG sums of samples. |
| aligninfo.numthreads | number of threads in alignment program. |
| aligninfo.verbose | Print verbose message |

5. genomescaninfo

This section defines parameters for CMS measurement construction.

| Parameter | Description |
|-------|-------|
| genomescaninfo.readextension | True to extend reads length before CMS measurement construction. |
| genomescaninfo.fragsize | the fixed fragment size to extend when readextension is True. |
| genomescaninfo.windowfile | an intermediate window file with fixed-size genomic regions. |
| genomescaninfo.referencename | the UCSC genome name to fetch reference genome size. E.g., hg38 or mm10. |
| genomescaninfo.windowsize | the window size |
| genomescaninfo.readscount | CMS measurement using read count (True) or mean WIG (False). |
| genomescaninfo.counttablefile | the result count table file. |
| genomescaninfo.verbose | Print verbose message |

6. dhmrinfo

Parameters in this section is for DMR detection.

| Parameter | Description |
|-------|-------|
| dhmrinfo.method | The statistical method used in DHMR detection. Available methods: `ttest`, `chisq`, `gtest`, `nbtest`, `nbtest_sf`. `ttest` is calling Student's t-test to examine the mean difference of CMS measurements between two biological groups. `chisq` and `gtest` are Pearson’s Chi-squared and G-test to test if sums of CMS measurements fit the numbers of replicates between two biological condtions. `nbtest` applies negative binomial generalized linear model to formulate CMS measurements, and Wald test evaluates the significance of logarithmic fold change. By default, CMS measurement are adjusted by size factors using spike-in normalization. In `nbtest_sf`, CMS measurements are normalized by the median-ratio algorithm (previously used in DESeq2 for transcriptome measurements). |
| dhmrinfo.meandepth | Average depth to filter out low-depth windows. This step is essential to save computing resources and increase power of downstream statistical inference |
| dhmrinfo.testfile | The result file with statistical outputs for whole genome windows |
| dhmrinfo.qthr | q-value threshod for DHMW. |
| dhmrinfo.maxdistance | Maximum distance to merge adjacent DHMWs into DHMRs |
| dhmrinfo.dhmrfile | The final DHMR result file after merging adjacent DHMWs. |
| dhmrinfo.numthreads | The number of threads. |
| dhmrinfo.nsplit | The number of split of windows. This option controls parallelization with `dhmrinfo.numthreads`. |
| dhmrinfo.verbose | Print verbose message. |
| dhmrinfo.keepNA | Keep genome windows ruled out by independent filtering. |

7. useinput

To indicate if the input data is used during CMS-IP sequencing.

8. inputinfo

If `useinput` is True, this section is required to specify input data. When input data is used, peak windows are identified first by comparing CMS measurements between group 1/2 and their input data. Then, the union of peak windows are tested for DHMR between group 1 and group 2.

| Parameter | Description |
|-------|-------|
| inputinfo.group1 | The label for the first group input data. |
| inputinfo.group2 | The label for the second group input data. Group 1 and group 2 can share same set of input data. |
| inputinfo.method | The statistical method used in peak calling. See `dhmrinfo.method`. |
| inputinfo.qthr | q-value threshold for peak calling. |
| inputinfo.testfile1 | Statistical test results for group 1 peaking calling. |
| inputinfo.dhmrfile1 | Peak regions for group 1. |
| inputinfo.testfile2 | Statistical test results for group 2 peaking calling. |
| inputinfo.dhmrfile2 | Peak regions for group 2. |
| inputinfo.inputfilterfile | Union of peak regions in group 1 and group 2. |
| inputinfo.verbose | Print verbose message. |

### A toy example using BAM inputs

To facilitate the running of HaMiP, a toy example is generated using existing BAM inputs. The example is accessible at https://github.com/lijinbio/HaMiP/blob/master/example. The `example` directory consists of running scripts and example BAM files. Below commands will generate the configuration file and run the example.

```
$ ./config.sh ## Generate config.yaml
$ ./fasta.sh ## download the reference genome and the spike-in genome under ./fasta
$ ./run.sh ## run the example
```

1. `config.sh`

This script will generate the running configuration file. The inspection of configuration file has been explained above. This example includes small BAM files for 2 KO and 2 WT samples, together with 3 input samples. Spike-in BAM files are also included for spike-in normalization. These BAM files are under the `./bamfile` directory. The `gtest` is used for peaking calling and DHMR detection.

2. `fasta.sh`

This script is to download required FASTA file for reference genome and spike-in genome. These FASTA files are used in MCALL for bisulfite conversion ratio (BCR) estimation. FASTA files are downloaded into a local directory `./fasta`.

3. `run.sh`

The simple command to run CMSIP:

```
$ HaMiP -c config.yaml
```

Intermediate and results files are stored under `./outdir`. The example quality control statistic file (e.g., `qcstats.txt`) is as below.

| sample_id | total | unique_ref | ref/total | unique_spk | spk/total | comm | comm/total | comm/unique_ref | twss_spk | sizefactors | twss_ref | twss_ref_norm | bcr_ref | bcr_spk |
|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|-------|
| T1 | 2328 | 2328 | 100.00% | 141 | 6.06% | 99 | 4.25% | 4.25% | 3053 | 0.52 | 171892 | 88620 | 0.022883 | 0.278465 |
| T2 | 20414 | 20414 | 100.00% | 2780 | 13.62% | 2539 | 12.44% | 12.44% | 9522 | 0.17 | 704965 | 116532 | 0.033482 | 0.178238 |
| W1 | 1588 | 1588 | 100.00% | 97 | 6.11% | 74 | 4.66% | 4.66% | 1786 | 0.88 | 118312 | 104268 | 0.043317 | 0.206362 |
| W2 | 1182 | 1182 | 100.00% | 89 | 7.53% | 66 | 5.58% | 5.58% | 1574 | 1.00 | 85335 | 85335 | 0.034864 | 0.214435 |
| I1 | 212 | 212 | 100.00% | 17 | 8.02% | 4 | 1.89% | 1.89% | 992 | 1.59 | 15984 | 25362 | 0.738502 | 0.811715 |
| I2 | 150 | 150 | 100.00% | 14 | 9.33% | 1 | 0.67% | 0.67% | 1032 | 1.53 | 11586 | 17671 | 0.897633 | 0.994475 |
| I3 | 52 | 52 | 100.00% | 9 | 17.31% | 0 | 0.00% | 0.00% | 356 | 4.42 | 2053 | 9077 | 0.910494 | 0.983871 |

Specifically, the `sizefactors` column is the size factors generated by spike-in normalization.

The example DHMR file is as below.

| chrom | start | end | baseMean | lfc | statistic | pvalue | padj |
|-------|-------|-------|-------|-------|-------|-------|-------|
| chr4 | 105276100 | 105276400 | 95.88 | -0.8072375451 | 27.63702666 | 1.463503254e-07 | 2.048904555e-06 |
| chr4 | 105272500 | 105272700 | 86.7175 | -0.837383035 | 19.45881901 | 1.027921214e-05 | 4.796965666e-05 |
| chr4 | 105259600 | 105259800 | 42.4925 | -0.5320182773 | 5.682020984 | 0.01713961427 | 0.03999243329 |

For example, three hypo-DHMRs are identified in chr4 between group T and group W.

## Contact

Maintainer: Jin Li, lijin.abc@gmail.com.
PI: De-Qiang Sun, dsun@tamu.edu.

