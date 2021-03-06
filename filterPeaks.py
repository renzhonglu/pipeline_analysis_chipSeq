__author__ = 'peeyush'


def filterpeaks(peak_data_list):
    filtered_peak_data = {}
    peak_data = peak_data_list
    file = open('/ps/imt/e/20141009_AG_Bauer_peeyush_re_analysis/further_analysis/filtered/filteredPeaksCount.txt', 'w')
    file.write('Sample_name\traw_peaks\tfiltered_peaks\n')
    for k, v in peak_data.iteritems():
        print k
        name = k
        df = v
        sample = name.split(' ')
        if "Encode" in sample[0]:
            final = df
        else:
            colnames = df.columns.values.tolist()
            indices1 = [i for i, s in enumerate(colnames) if sample[0] in s]
            indices2 = [i for i, s in enumerate(colnames) if sample[2] in s]
            indices3 = [i for i, s in enumerate(colnames) if "Input" in s]
            print indices1
            for i in indices1:
                if "RA" not in colnames[i] and "RA" not in name and "norm" not in colnames[i]:
                    condition = colnames[i]
                    break
                elif "RA" in colnames[i] and "RA" in name and "norm" not in colnames[i]:
                    condition = colnames[i]
                    break
            else:
                raise ValueError("Filtering Error: Sample name differs from column name.")

            print condition
            control = colnames[indices2[0]]
            print control
            inputcol = colnames[indices3[0]]
            print inputcol
            if "Sample" in sample[0]:
                df1 = df[df[condition] >= 3*df[control]]
                df2 = df1[((df1['stop']-df1['start'])/df1[condition]) <= 15]
                final = df2
            elif "H3R2" in sample[0] or "YY1" in sample[0]:
                df1 = df[df[condition] >= 5*df[inputcol]]
                final = df1[df1[condition] >= 3*df1[control]]
                #final = df
            elif "PRMT6" in sample[0] and "RA" in sample[0]:
                #df1 = df[df[condition] >= 5*df[inputcol]]
                df2 = df[df[condition] >= 3*df[control]]
                df3 = df2[((df2['stop']-df2['start'])/df2[condition]) <= 10]
                final = df3[df3[colnames[indices1[0]]] >= 50]
            elif "PRMT6" in sample[0]:
                #df1 = df[df[condition] >= 4*df[inputcol]]
                df2 = df[df[condition] >= 3*df[control]]
                df3 = df2[((df2['stop']-df2['start'])/df2[condition]) <= 15]
                final = df3[df3[condition] >= 50]
            else:
                df1 = df[df[condition] >= 5*df[inputcol]]
                df2 = df1[df1[condition] >= 3*df1[control]]
                final = df2[df2[condition] >= 50]
        file.write(name.split(' ')[0]+'\t'+str(len(df))+'\t'+str(len(final))+'\n')
        filtered_peak_data[name] = final
        final.to_csv('/ps/imt/e/20141009_AG_Bauer_peeyush_re_analysis/further_analysis/filtered/filtered'+name+'.csv', sep=",", encoding='utf-8')
    file.close()
    return filtered_peak_data
