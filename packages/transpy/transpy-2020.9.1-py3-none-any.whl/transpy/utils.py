import numpy as np
import pandas as pd
import geopandas as gpd

from shapely import ops
from pyproj.crs import CRS
from multiprocessing import Pool
from typing import Any, List, Union, Iterable
from shapely.geometry import LineString, MultiLineString


def to_chunk(in_iterator: Iterable, **kwargs) -> List[List[Any]]:
    """
    Splits an iterator into multiple sub iterator based on the provided chunk size. The iterator must be slice-able. The
    last chunk might have less number of elements in it.

    :param in_iterator: The input iterator to be chunked into parts. It must be possible to call it using slices.

    :type in_iterator: Iterable

    :param kwargs: a dictionary defining how to determine the chunk size or number of chunks.
                   Possible values are:

                   - `chunk_size`: a positive non-zero integer defining the number of elements in each chunk

                   - `n_chunk`: number of chunks. The chunk_size is determined based on the number of elements in the iterator.

                   - `pool`: a parallel pool of workers. Based on the number of workers available in the pool the iterator is divided.

    :return: a list containing multiple sub-list which holds the elements in the iterator.

    """
    input_as_list = list(in_iterator)
    nelem = len(input_as_list)

    if 'chunk_size' in kwargs:
        chunk_size = int(kwargs.get('chunk_size'))
    elif 'n_chunk' in kwargs:
        chunk_size = int(nelem / kwargs.get('n_chunk'))
    elif 'pool' in kwargs:
        n_process = kwargs['pool']._processes
        chunk_size = int(nelem / n_process)
    else:
        raise ValueError('Could not determine chunk_size.')

    if chunk_size < 1:
        raise ValueError(f'chunk_size={chunk_size} is invalid.')

    output = [input_as_list[i:i+chunk_size] for i in range(0, nelem, chunk_size)]
    return output


def split_linestring(
        geometry: Union[LineString, MultiLineString, Iterable],
        max_length: float,
        pool: Pool = None) -> Union[List[LineString], List[List[LineString]]]:
    """
    Splits a LineString into smaller parts with equal length not exceeding max_length. NOTE: the length must be provided
    in an appropriate unit as of the one used in LineString coordinate system. If the input geometry is a
    MultiLineString each LineString geometry is divided. If the input geometry is neither a LineString nor a
    MultiLineString the same geometry is returned within the list.

    :param geometry: The LineString object needs splitting

    :param max_length: The maximum length that each split will have. NOTE: The actual length would not exceed this
                       value.

    :param pool: a process pool to be used for parallelism. The pool is only used if the geometry is of type iterable.

    :return: a list of LineString Object if the input is LineString or MultiLineString; or a list of list of LineString,
             if the input geometry is an iterable of LineString and MultiString.

    """
    output = None
    if isinstance(geometry, LineString):
        length = geometry.length
        n_parts = int(np.ceil(length/max_length))
        fractions = np.linspace(0, 1, n_parts + 1)
        output = [
            ops.substring(geometry, start_fraction, end_fraction, normalized=True)
            for start_fraction, end_fraction in zip(fractions[:-1], fractions[1:])
        ]
    elif isinstance(geometry, MultiLineString):
        output = []
        for linestring in geometry.geoms:
            output.extend(split_linestring(linestring, max_length))
    elif isinstance(geometry, Iterable):  # make sure this is listed after LineString & MultiLineString
        if pool is not None:  # PARALLEL
            # print('PARALLEL')
            chunked_geometry = to_chunk(geometry, pool=pool)
            pool_output = [
                pool.apply_async(
                    split_linestring,
                    (chunk, max_length)
                ) for chunk in chunked_geometry
            ]

            output = []
            for e in pool_output:
                output.extend(e.get())
        else:  # SERIAL
            # print('SERIAL')
            output = [
                split_linestring(e, max_length)
                for e in geometry
            ]

    else:
        output = [geometry]

    return output


def split_linestring_df(
        df: Union[pd.DataFrame, gpd.GeoDataFrame],
        max_length: float,
        pool: Pool = None,
        **kwargs) -> gpd.GeoDataFrame:
    """
    Splits the LineString existing in a data frame based on the provided `max_length`. All the other columns are
    retpeated untouched.

    :param df: The input `DataFrame` or `GeoDataFrame`

    :param max_length: The maximum length that each LineString is allowed to have. Has not effect on other geometry t
                       types.

    :param pool: A pool of parallel workers to speed up processing large data frames.

    :param kwargs: Extra keywords controlling the behavior of this function. Currently available keywords are:

                   - 'length_epsg`: the EPSG that the max_length is provided. The default is EPSG:3857 hence, the
                     `max_length` is assumed to be meter.
                   - `geom_field`: The name of the column containing the geometry. Default is 'geometry'.
                   - `part_id_field`: The name of the columns to be added to the output which identifies different parts
                     of the same geometry. Default is `part_id`.

    :return: a new `GeoDataFrame` where LineString or MultiLineStrings do not exceed the `max_length`
    """
    length_epsg = kwargs.get('length_epsg', 3857)
    length_crs = CRS(length_epsg)
    original_crs = None if length_crs.name == df.crs.name else df.crs
    df = df if length_crs.name == df.crs.name else df.to_crs(length_crs)

    geom_field = kwargs.get('geom_field', 'geometry')
    split_geometry = split_linestring(
        geometry=df[geom_field],
        max_length=max_length,
        pool=pool
    )

    part_id_field = kwargs.get('part_id_field', 'part_id')
    output = pd.concat([
        gpd.GeoDataFrame(
            data={
                key: (
                    [row[1][key]] * len(split_geometry[row[0]]) \
                    if key != part_id_field \
                    else list(range(len(split_geometry[row[0]])))
                )
                for key in list(row[1].keys()) + [part_id_field] if key != geom_field
            },
            geometry=split_geometry[row[0]]
        )
        for row in df.iterrows()
    ])

    output.reset_index(drop=True, inplace=True)
    output.crs = length_crs

    if original_crs is not None:
        output = output.to_crs(original_crs)

    return output
