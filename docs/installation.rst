Installation Guide
==================


Download
********
Simply download this "metapackage_" to your workspace and build it.


.. code-block:: sh

  cd ~/xxx_ws/src      # cd to your workspace
  mkdir Xicro          # create metapackage 
  cd Xicro             # cd to metapackage
  git clone https://github.com/imchin/Xicro .
  cd ~/xxx_ws
  colcon build
  source ~/xxx_ws/install/setup.bash

.. _metapackage: https://github.com/imchin/Xicro/

Requirements
************
The requirements for running this project are:
  - Pyserial_
  - Numpy_


.. _Pyserial: https://pythonhosted.org/pyserial/
.. _Numpy: https://numpy.org/devdocs/reference/index.html#reference