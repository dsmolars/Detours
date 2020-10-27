import os
import subprocess
import winreg

CMAKE_VS_MSBUILD_COMMAND = os.path.join(
    os.environ['ProgramFiles(x86)'],
    'Microsoft Visual Studio',
    '2019',
    'Professional',
    'MSBuild',
    'Current',
    'Bin',
    'MSBuild.exe')

VS_INSTALL_DIR = os.path.abspath(os.path.join(
    os.path.dirname(CMAKE_VS_MSBUILD_COMMAND), '..', '..', '..'))
VS_VCVARS_32 = os.path.join(
    VS_INSTALL_DIR, 'VC', 'Auxiliary', 'Build', 'vcvars32.bat')
VS_VCVARS_64 = os.path.join(
    VS_INSTALL_DIR, 'VC', 'Auxiliary', 'Build', 'vcvars64.bat')

if '__main__' == __name__:
    config = 'release'
    architecture = 'x64'
    nmake_build_batch_path = os.path.abspath(os.path.join(
        'build', 'output', 'windows', config, architecture, 'nmake_build.bat'))
    os.makedirs(os.path.dirname(nmake_build_batch_path),
                exist_ok=True, mode=0o644)
    with open(nmake_build_batch_path, 'w+') as nmake_build_batch:
        nmake_build_batch.write(
            'pushd {0}\n'.format(os.path.abspath(os.path.dirname(__file__))))
        if 'x64' == architecture:
            nmake_build_batch.write('call "{0}"\n'.format(VS_VCVARS_64))
        elif 'x86' == architecture:
            nmake_build_batch.write('call "{0}"\n'.format(VS_VCVARS_32))
        else:
            raise Exception('Unsupported architecture', architecture)
        nmake_build_batch.write('nmake\n')
        nmake_build_batch.write('popd\n')
    nmake_result = subprocess.run(
        [nmake_build_batch_path],
        cwd=os.path.dirname(nmake_build_batch_path),
        capture_output=True)
    if 0 == nmake_result.returncode:
        print(nmake_result.stdout.decode('utf-8'))
    else:
        print(nmake_result.stderr.decode('utf-8'))
        raise Exception('NMake build failed')
