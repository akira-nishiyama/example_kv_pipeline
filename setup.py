from setuptools import setup

package_name = 'example_kv_pipeline'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='anishiyama',
    maintainer_email='mr081677@gmail.com',
    description='TODO: Package description',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'node1 = example_kv_pipeline.node1:main',
            'node2 = example_kv_pipeline.node2:main',
            'node3 = example_kv_pipeline.node3:main',
        ],
    },
)
