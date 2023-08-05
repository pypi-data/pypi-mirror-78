import pandas as pd
from loguru import logger as log
import os



def concat_csv_files(input_pathname, output_filepath, overwrite=False):
    """
    Concatenates CSV files from a specified directory
    :param input_pathname: Directory containing CSV files
    :param output_filepath: Full filepath of the output CSV file
    :return: None
    """
    if os.path.exists(output_filepath) and not overwrite:
        raise FileExistsError('Output file exists. To overwrite, set overwrite=False')

    frames = []
    for filename in sorted(os.listdir(input_pathname)):
        if filename.endswith('.csv'):

            log.info(f'Processing file: {filename}')
            filepath = os.path.join(input_pathname, filename)
            df = pd.read_csv(filepath)
            frames.append(df)

    log.info('Concatenating CSV files')
    df = pd.concat(frames)

    log.info('Saving output file')
    df.to_csv(output_filepath)

    log.info('Process completed')

if __name__ == '__main__':
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    out_dir = os.path.dirname(data_dir)
    out_fp = os.path.join(out_dir, 'concatenated.csv')
    concat_csv_files(data_dir, out_fp)