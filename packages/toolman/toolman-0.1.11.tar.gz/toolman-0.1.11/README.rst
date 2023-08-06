*****************************************
ToolMan: Python utility functions for R&D
*****************************************

.. image:: https://img.shields.io/pypi/v/toolman.svg
   :target: https://pypi.python.org/pypi/toolman/

.. image:: https://travis-ci.com/bohaohuang/toolman.svg?branch=master
  :target: https://travis-ci.com/bohaohuang/toolman

.. image:: https://codecov.io/gh/bohaohuang/toolman/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/bohaohuang/toolman

See the source for this project on our `GitHub page <https://github.com/bohaohuang/toolman>`_

Install
#######
.. code-block:: bash

    pip install toolman

Modules
#######
`mist_utils.py <./toolman/misc_utils.py>`_
*******************************************
miscellaneous utility functions including data I/O and processing

a) Read/write different formats of files in one function:

.. code-block:: python

    import toolman as tm
    data = tm.misc_utils.load_file(file_name)
    tm.misc_utils.save_file(file_name, data)

Currently support extensions including: `.npy`, `.pkl`, `.txt`, `.csv`, `.json` and commonly used image formats.

b) Argument parser, parse nested argument list:

.. code-block:: python

    import sys
    import argparse
    import toolman as tm
    parser = argparse.ArgumentParser()
    args, extras = parser.parse_known_args(sys.argv[1:])
    cfg_dict = tm.misc_utils.parse_args(extras)

`vis_utils.py <./toolman/vis_utils.py>`_
*******************************************
Matplotlib utility functions for visualization

a) Display images in side by side with axis linked

.. code-block:: python

    import toolman as tm
    fig1 = tm.misc_utils.load_file(img_name_1)
    fig2 = tm.misc_utils.load_file(img_name_1)
    tm.vis_utils.compare_figures([fig1, fig2], (1, 2), fig_size=(12, 5))

b) Display barplots

.. code-block:: python

    import toolman as tm
    data = np.random.random((3, 4))
    labels = ['group 1', 'group 2', 'group 3']
    xticks = ['cluster 1', 'cluster 2', 'cluster 3', 'cluster 4']
    tm.vis_utils.compare_bars(data, labels, xticks)


`img_utils <./toolman/img_utils.py>`_
*******************************************
image specific utility functions

`pytorch_utils <./toolman/pytorch_utils.py>`_
**************************************************
pytorch specific utility functions

`process_block <./toolman/process_block.py>`_
*************************************************
A processing unit that do certain operations only if it has never done before. This is helpful avoid duplicate
executing time consuming jobs.

.. code-block:: python

    import toolman as tm
    def foo(cnt_len):
        cnt = 0
        for i in range(cnt_len):
            cnt += 1
        return cnt

    pb = tm.process_block.ProcessBlock(foo, file_dir)
    pb.run(force_run=False, cnt_len=100)
