import os
import pandas as pd
import logging
from logger import setup_logger


def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_csv_path():
    return os.path.join(get_project_root(), 'data', 'pedidos.csv')


def load_csv(csv_path):
    if not os.path.exists(csv_path):
        raise FileNotFoundError("FILE_NOT_FOUND")

    df = pd.read_csv(csv_path)

    if df.empty:
        raise ValueError("EMPTY_FILE")

    return df


def prepare_freight_queue(df):
    if 'data_embarque' not in df.columns:
        raise KeyError("COLUMN_NOT_FOUND")

    df['data_embarque'] = pd.to_datetime(
        df['data_embarque'],
        format='%d/%m/%Y',
        errors='coerce'
    )

    if df['data_embarque'].isnull().any():
        raise ValueError("INVALID_DATE")

    return df.sort_values('data_embarque')


def save_to_excel(df):
    output_path = os.path.join(
        get_project_root(),
        'data',
        'fila-fretes.xlsx'
    )

    df.to_excel(output_path, index=False)
    return output_path


def main():
    setup_logger()
    logging.info("START")

    try:
        logging.info("LOAD")
        df = load_csv(get_csv_path())

        logging.info("TRANSFORM")
        df = prepare_freight_queue(df)

        logging.info("EXPORT")
        save_to_excel(df)

        logging.info("END")

    except FileNotFoundError:
        logging.error("FILE_NOT_FOUND")
    except KeyError:
        logging.error("COLUMN_NOT_FOUND")
    except ValueError as e:
        logging.error(str(e))
    except Exception as e:
        logging.error(f"ERROR: {e}")


if __name__ == "__main__":
    main()
