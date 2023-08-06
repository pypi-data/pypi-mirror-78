from setuptools import setup, find_packages

setup(
    name="iotile_support_prod_pod1m_1",
    packages=find_packages(include=["iotile_support_prod_pod1m_1.*", "iotile_support_prod_pod1m_1"]),
    version="1.3.1",
    install_requires=['numpy >= 1.15.1', 'sortedcontainers ~= 2.1', 'iotile-core ~= 5.0', 'iotile-ext-cloud ~= 1.0', 'iotile-sensorgraph ~= 1.0'],
    entry_points={'iotile.virtual_device': ['pod_1m = iotile_support_prod_pod1m_1.pod_1m'], 'iotile.app': ['tracker_app = iotile_support_prod_pod1m_1.tracker_app'], 'iotile.recipe_action': ['CalibratePOD1MStep = iotile_support_prod_pod1m_1.CalibratePOD1MStep:CalibratePOD1MStep', 'ResetPOD1MStep = iotile_support_prod_pod1m_1.ResetPOD1MStep:ResetPOD1MStep']},
    include_package_data=True,
    author="Arch",
    author_email="info@arch-iot.com"
)