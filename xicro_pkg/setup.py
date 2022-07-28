from setuptools import setup

package_name = 'xicro_pkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    py_modules=[
    	'scripts.gui_xicro',
#xicro1
	"scripts.generate_Xicro_node",
	"scripts.generate_arduino_lib",
#2orcix
    ],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='imchin',
    maintainer_email='imarkchin@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        	"xicro_gui_node = scripts.gui_xicro:main",
#xicro1
		"xicro_generate_Xicro_node = scripts.generate_Xicro_node:main",
		"xicro_generate_arduino_lib = scripts.generate_arduino_lib:main",
#1orcix
        ],
    },
)
