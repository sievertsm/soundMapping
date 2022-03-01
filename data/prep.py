def read_sound_timeHistory(p, offset=0, octave=False):
    # read data
    if octave:
        data = pd.read_excel(p, sheet_name=5)
    else:
        data = pd.read_excel(p, sheet_name=3)

    # identify runs
    run_mask = data['Record Type'].values == 'Run'
    # create number label for run
    run_id = np.arange(offset, run_mask.sum()+offset)

    # apply run number ID to dataframe
    data['Run ID'] = np.nan
    data.loc[run_mask, 'Run ID'] = run_id
    data['Run ID'] = data['Run ID'].ffill()

    data['Run ID'] = data['Run ID'].astype(int)
    
    offset = run_id.max()+1
    
    return data, offset


def read_sound_octaveBand(p, oneThird=False):
    # set number of rows to skip to read the correct data
    skiprow=7 if oneThird else 1
    
    # read data
    data = pd.read_excel(p, sheet_name=1, skiprows=skiprow, nrows=3)
    # format data in "tidy" format
    data = data.T.dropna()
    data = data.reset_index()
    data.columns = data.iloc[0]
    data = data.drop(0, axis=0).reset_index(drop=True)
    
    return data


