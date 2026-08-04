import subprocess
import time
import argparse

def pull_data_and_decode(input_remote_directory:str, output_local_directory:str, track_but_not_decoded_list:list):
    decode_list = []
    linux_in_dir = '/'.join(input_remote_directory.split('\\'))
    if linux_in_dir[:39]!='debian@[fe80::6e30:2aff:febe:9859%eth0]':
        linux_in_dir=linux_in_dir.split(':')[1]
        linux_in_dir=':'.join(['debian@[fe80::6e30:2aff:febe:9859%eth0',linux_in_dir])

    result = subprocess.run(
                ["wsl", "sshpass", "-p", "gs66c235","rsync", "-avz", "--progress", "--out-format=%n", f"{linux_in_dir}", f"{output_local_directory}"],
                capture_output=True,
                text=True
            )
    windows_out_dir='\\'.join(output_local_directory.split('/'))
    result_list=[windows_out_dir+i for i in result.stdout.splitlines() if (('.' in i[-6:]) and (i[-1] not in ['0','1','2','3','4','5','6','7','8','9','.']))]

    for item in track_but_not_decoded_list:
        if item not in result_list:
            decode_list.append(item)

    track_but_not_decoded_list=[i for i in result_list]

    for file_name in decode_list:
        if file_name[-6:] == 'hk.bin':
            subprocess.run(['python', 'astep_housekeeping_decoder.py', f'{file_name}', '--not-live', '--influx'])
            # run_subprocess_hk_decode_and_send_to_influx
        elif file_name[-4:] == '.bin':
            # run_subprocess_bin_decode_and_send_to_influx
            subprocess.run(['python', 'QuadChip_PostDecode.py', f'{file_name}'])

    

    return track_but_not_decoded_list

def main(args):
    # decode_list=[]
    # print(args.output)
    # result = subprocess.run(
    #     ["sshpass", "-p", "gs66c235","rsync", "-avz", "--progress", "--out-format=%n", f"{args.input}", f"{args.output}"],
    #     capture_output=True,
    #     text=True
    # )
    result = subprocess.run(
            ["wsl", "sshpass", "-p", "gs66c235","rsync", "-avz", "--progress", "--out-format=%n", f"{args.input}", f"{args.output}"],
            capture_output=True,
            text=True
        )
    # print(result)
    windows_out_dir='\\'.join(args.output.split('/'))
    # print(windows_out_dir)
    result_list=[windows_out_dir+i for i in result.stdout.splitlines() if (('.' in i[-6:]) and (i[-1] not in ['0','1','2','3','4','5','6','7','8','9','.']))]
    track_but_not_decoded_list=[i for i in result_list]
    try:
        while True:
            print('waiting 10 seconds...')
            time.sleep(10)
            track_but_not_decoded_list = pull_data_and_decode(args.input, args.output, track_but_not_decoded_list)

    except KeyboardInterrupt as KI:
        print(KI)
        print('Exiting cleanly...')
        track_but_not_decoded_list = pull_data_and_decode(args.input, args.output, track_but_not_decoded_list)
        print('All done')


if __name__=='__main__':
    parser = argparse.ArgumentParser(
        description='Program to pull data from beagle bone, decode data that is done being pulled, and send it to influx'
    )
    parser.add_argument(
        '-i',
        '--input',
        type=str,
        required=True,
        help='Input remote directory to pull data from, required, no default'
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        required=True,
        help='Output local directory that data is copied to and decoded to, required, no default'
    )
    args = parser.parse_args()
    main(args)