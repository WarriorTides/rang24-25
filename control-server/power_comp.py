## does nothing at the moment

from pprint import pprint


power_dict = {}
with open("./power.csv", "r") as file:
    lines = file.readlines()
    for val in lines:
        pwm = int(val.split(",")[0].strip())
        val = float(val.split(",")[1].strip())
        for i in range(-2, 2):
            power_dict[pwm - i] = val

    file.close()


def pwm_to_amps(pwm_arr):
    ampcount = 0.0
    for i in pwm_arr:
        ampcount += power_dict[i]
    return ampcount


def power_to_amps(power_arr, maxThrottle):
    ampcount = 0.0
    for i in power_arr:
        ampcount += power_dict[mapnum(i, -1, 1, 1100, 1900)]
    return ampcount


def calcnew(pwm_arr, maxAMP):
    ampcount = 0.0
    newarr = []
    ampcount = pwm_to_amps(pwm_arr)
    print("Original aps:" + str(ampcount))
    if ampcount > maxAMP:
        while ampcount > maxAMP:
            while ampcount > maxAMP:
                # Scale down each PWM value slightly
                for i in range(len(pwm_arr)):
                    if pwm_arr[i] > 1500:
                        pwm_arr[i] -= 1
                    else:
                        pwm_arr[i] += 1
                        # newarr.append(pwm_arr
                # Recalculate total amps
                ampcount = pwm_to_amps(pwm_arr)
    else:
        return pwm_arr
    ampcount = 0
    for i in newarr:
        ampcount += power_dict[i]
    print("Final aps:" + str(ampcount))
    return pwm_arr


if __name__ == "__main__":
    print(calcnew([1315, 1200, 1200, 1200, 1500, 1500, 1500], 10))
