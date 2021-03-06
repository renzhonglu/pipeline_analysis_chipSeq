import overlapping_analysis

__author__ = 'peeyush'
from pandas import read_csv
import pandas as pd
import cal_genomic_region
import filterPeaks
import seqOperations
import os
import time


#time.strftime("%d/%m/%y")

folders = ["overlap",
           "differential",
           "filtered",
           "plots",
           "seq4motif",
           "valley_peaks",
           "CpG"]
for folder in folders:
    print 'Directory_for_result: ' + '/ps/imt/e/20141009_AG_Bauer_peeyush_re_analysis/further_analysis/'+folder
    path = '/ps/imt/e/20141009_AG_Bauer_peeyush_re_analysis/further_analysis/'+folder
    if not os.path.exists(path):
        os.makedirs(path)

sample_name = [#'YY1_RA_seq3 vs IgG_RA_seq2 filtered',
               #'YY1_seq2 vs IgG_seq2 filtered',
               #'YY1_RA_seq2 vs IgG_RA_seq2 filtered',
               #'PRMT6_2_seq4 vs IgG_seq4 filtered',
               #'H3R2me2_18F3_seq7 vs IgG_seq4 filtered',
               #'H3R2me2_17E2_seq7 vs IgG_seq4 filtered',
               'PRMT6_2_seq6 vs IgG_seq6 filtered',
               #'PRMT6_2_RA_seq2 vs IgG_RA_seq2 filtered',
               #'PRMT6_2_seq3 vs IgG_seq2 filtered',
               #'PRMT6_2_RA_seq3 vs IgG_seq2 filtered',
               #'H3R2me2_17F10_seq7 vs IgG_seq4 filtered',
               #'H3R2me2_17H5_seq7 vs IgG_seq4 filtered',
               #'JARID1A_seq2 vs IgG_seq2 filtered',
               #'PRMT6_2_RA_seq6 vs IgG_RA_seq6 filtered',
               #'JARID1A_RA_seq2 vs IgG_RA_seq1 filtered',
               #'H3K27me3_seq2 vs IgG_seq2 filtered',
               #'PRMT6_2_seq1 vs IgG_seq1 filtered',
               #'PRMT6_2_seq5 vs IgG_seq2 filtered',
               #'YY1_seq3 vs IgG_seq2 filtered',
               #'PRMT6_2_seq2 vs IgG_seq2 filtered',
               #'PRMT6_2_RA_seq5 vs IgG_RA_seq2 filtered',
               #'PRMT6_2_RA_seq4 vs IgG_RA_seq4 filtered',
               #'H3K27me3_RA_seq2 vs IgG_RA_seq2 filtered',
               #'H3K4me3_RA_seq2 vs IgG_RA_seq2 filtered',
               #'PRMT6_2_RA_seq1 vs IgG_RA_seq1 filtered',
               #'H3K4me3_seq2 vs IgG_seq2 filtered',
               #'Encode_NT2D1_H3K36me3',
               #'Encode_NT2D1_Suz12 vs Input',
               #'Sample_18F3_RA vs IgG_RA_seq6 filtered',
               #'Sample_18F3 vs Sample_8C9 filtered',
               #'Sample_K27ac vs Sample_8C9 filtered',
               #'Sample_EZH1_RA vs IgG_RA_seq6 filtered',
               #'Sample_EZH1 vs Sample_8C9 filtered',
               #'Sample_EZH2_RA vs IgG_RA_seq6 filtered',
               #'Sample_EZH2 vs Sample_8C9 filtered',
               #'Sample_H3R2_comm_RA vs IgG_RA_seq6 filtered',
               #'Sample_H3R2_comm vs Sample_8C9 filtered',
               #'Sample_K4me1_RA vs IgG_RA_seq6 filtered',
               #'Sample_K4me1 vs Sample_8C9 filtered',
               #'Sample_K9me3_RA vs IgG_RA_seq6 filtered',
               #'Sample_K9me3 vs Sample_8C9 filtered',
               #'Sample_K27ac_RA vs IgG_RA_seq6 filtered',
               #'Sample_K27me3_RA vs IgG_RA_seq6 filtered',
               #'Sample_K27me3 vs Sample_8C9 filtered',
               #'Sample_K36me3_RA vs IgG_RA_seq6 filtered',
               #'Sample_K36me3 vs Sample_8C9 filtered',
               #'Sample_pol-2_RA vs IgG_RA_seq6 filtered',
               #'Sample_pol-2 vs Sample_8C9 filtered',
               #'Sample_PRMT6_3_RA vs IgG_RA_seq6 filtered'
               ]

# Here import peak called data in a list....
peak_data = {}
for a in sample_name:
    df = read_csv(
        '/ps/imt/e/20141009_AG_Bauer_peeyush_re_analysis/csv/' + a + '.csv',
        header=0, sep='\t')
    df = df.rename(columns={'Next Gene name': 'Next transcript gene name'})
    peak_data[a] = df
print "Number of sample are being analysed: ", peak_data.__len__()

print "Filtering peaks."
filtered_peak_data = filterPeaks.filterpeaks(peak_data)

peakAnalysis_df = {}
for k, v in filtered_peak_data.iteritems():
    name = k
    df = v
    GR_analysis = cal_genomic_region.PeaksAnalysis(df, name)
    cal_genomic_region.genomic_regions(GR_analysis)
    peakAnalysis_df[name] = GR_analysis

# Performing motif and CpG analysis on prmt6 sites wrt regions

sample_dict = {}
prmt6_df = filtered_peak_data.get('PRMT6_2_seq6 vs IgG_seq6 filtered')
for i in ['tss', 'exon', 'intron', 'intergenic']:
    sample_dict['PRMT6_Non_RA_'+i] = prmt6_df[prmt6_df['GenomicPosition TSS=1250 bp, upstream=5000 bp'] == i]
seq = seqOperations.seq4motif(sample_dict)
db = ["JASPAR_CORE_2014_vertebrates.meme", "uniprobe_mouse.meme"]
seqOperations.motif_analysis(db, 10, seq)



'''
overlapping_samples = {}

sample_name1 = ['PRMT6_2_seq6 vs IgG_seq6 filtered', 'PRMT6_2_RA_seq6 vs IgG_RA_seq6 filtered']#, 'PRMT6_2_RA_seq6 vs IgG_RA_seq6 filtered']
sample_name2 = ['H3K4me3_seq2 vs IgG_seq2 filtered', 'H3K4me3_RA_seq2 vs IgG_RA_seq2 filtered']#, 'Sample_18F3_RA vs IgG_RA_seq6 filtered']

if len(sample_name1) != len(sample_name2):
    raise ValueError("Unequal sample list for comparison")
else:
    overlap = 0
    for i in range(0, len(sample_name1)):
        overlapping_res = cal_genomic_region.OverlappingPeaks(peakAnalysis_df, sample_name1[i], sample_name2[i])
        name = overlapping_res.keys()[0]
        with open("/ps/imt/e/20141009_AG_Bauer_peeyush_re_analysis/further_analysis/overlap/overlapping_peaks.txt", "a") as file:
            file.write(
                name.split('vs')[0] + '\t' + name.split('vs')[2][1:] + '\t' + str(len(overlapping_res.get(name))) + '\n')
        if len(overlapping_res.get(name)) >= 1:
            overlapping_obj = overlapping_analysis.Overlaps(overlapping_res, peak_data, filtered_peak_data)
            overlapping_analysis.diffBinding(overlapping_obj)

            #if sample_name1[i].split('_')[0] == sample_name2[i].split('_')[0]:
            unique_peaks = overlapping_analysis.non_overlapping_peaks(overlapping_obj, overlap)
            overlapping_samples['Unique_'+str(overlap)+'_'+sample_name1[i]] = unique_peaks[0]
            overlapping_samples['Unique_'+str(overlap)+'_'+sample_name2[i]] = unique_peaks[1]
            #overlapping_samples['Unchanged_'+sample_name1[i]+'_vs_'+sample_name2[i]] = unique_peaks[2]
            print overlapping_res.keys()[0]
            overlapping_samples.update({overlapping_res.keys()[0]: pd.DataFrame(overlapping_res.get(overlapping_res.keys()[0]))})
        overlap += 1


sample_name3 = ['PRMT6_2_seq6 vs IgG_seq6 filtered_vs_H3K4me3_seq2 vs IgG_seq2 filtered']
sample_name4 = ['Encode_NT2D1_H3K36me3']


diff_sample = ['PRMT6_2_seq6 vs IgG_seq6 filtered_vs_H3K4me3_seq2 vs IgG_seq2 filtered'] ## load samples to analysis


#peak_data2 = {}
for a in diff_sample:
    df = read_csv(
        '/ps/imt/e/20141009_AG_Bauer_peeyush_re_analysis/further_analysis/overlap/' + a + '.csv',
        header=0, sep=',')
    names_list = a.split('/')
    if len(names_list) > 1:
        a = names_list[len(names_list)-1]
    GPcount = df['GenomicPosition TSS=1250 bp, upstream=5000 bp'].value_counts()
    GPcount = zip(GPcount.index, GPcount.values)
    cal_genomic_region.plotGenomicregions(GPcount, a)
    overlapping_samples[a] = df
    print a

for i in range(0, len(sample_name3)):
    print 'Re-overlapping:', sample_name3[i], '======', sample_name4[i]
    overlap4diff = cal_genomic_region.overlappingPeaksLess(overlapping_samples, filtered_peak_data, sample_name3[i], sample_name4[i])
    name = overlap4diff.keys()[0]
    with open("/ps/imt/e/20141009_AG_Bauer_peeyush_re_analysis/further_analysis/overlap/overlapping_peaks.txt", "a") as file:
        file.write(
            name + '\t' + str(len(overlap4diff.get(name))) + '\n')
    overlapping_samples[overlap4diff.keys()[0]] = pd.DataFrame(overlap4diff.get(overlap4diff.keys()[0]))

for k, v in overlapping_samples.iteritems():
    if len(v) > 0:
        GPcount = v['GenomicPosition TSS=1250 bp, upstream=5000 bp'].value_counts()
        GPcount = zip(GPcount.index, GPcount.values)
        cal_genomic_region.plotGenomicregions(GPcount, k)

#sample_4_motif = ['Diff_peaks_Non_RA']

#for i in sample_4_motif:
#    overlapping_samples[i] = read_csv('/ps/imt/e/20141009_AG_Bauer_peeyush_re_analysis/further_analysis/differential/'+i+'.csv', header=0, sep=',')

 #this will make seq from Genomic regions
#print "Samples for seq fetching:", len(overlapping_samples)
#seq = seq4motif.seq4motif(overlapping_samples)
#db = ["JASPAR_CORE_2014_vertebrates.meme", "uniprobe_mouse.meme"]
#seq4motif.motif_analysis(db, 10, seq)
'''

