from image_analyzer_video import corner_analysis

file = "AnotherReality-WIP-20190425_20148x858-239-24p-Rec709-g24-48nits-dark_20_APR422HQ.mov"
detected_frame = "Frame 144 False" + "\n"
n = 1
path = "/images"
frame = 145

# write log file, expects string for variable detected_frame to write (append <= a) it into log file
def log(detected_frame):

    log_file = open("log_file.txt", "a")
    log_file.write(detected_frame)
    log_file.close()
    return True

def log_a(detected_frame):
    with open("log_file.txt", "a") as log_file:
        log_file.write(detected_frame + "\n")

def truncate_log(file_name = "log_file.txt"):
    with open(file_name, "r") as log_file:

        for line in log_file:
            frame = int(line.split()[-1])
            log_file_dict[frame] = line

        keys = list(log_file_dict.keys())

        for i in range(len(keys())):
            keys[i] - keys[i-1] == 1

#        then delete the second key and value by using the dictionary argument
            del log_file_dict





#def analyse_log_file():
    # read log file, then parse log file frame numbers (only)
    # save frame numbers in array and check for "consecutive numbers"
    # maybe shrink them in another array o.a.
#
