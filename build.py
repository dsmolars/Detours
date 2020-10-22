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
    nmake_commands = ['"', VS_VCVARS_64, '" && ', 'nmake', ' && ', 'exit']
    nmake_process = subprocess.Popen(
        'cmd /K " {0} "'.format(''.join(nmake_commands)),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        # cwd=os.environ['TEMP']
    )
    MAX_TIMEOUT_COUNT = 32
    timeout_counter = 0
    while MAX_TIMEOUT_COUNT > timeout_counter:
        try:
            nmake_process.wait(timeout=1)
            nmake_stdout, nmake_stderr = nmake_process.communicate()
            print(nmake_stdout.decode('utf-8'))
            print(nmake_stderr.decode('utf-8'))
        except subprocess.TimeoutExpired as timeout_expired:
            print('nmake build', timeout_counter, 'sec')
        timeout_counter = timeout_counter + 1
    nmake_process.kill()
    if nmake_process.returncode is None:
        print('NMake build process terminated')
    elif 0 != nmake_process.returncode:
        print('NMake build failed')
    else:
        print('NMake build succeeded')
