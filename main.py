from numpy import array, zeros, max, argmax, loadtxt, sum, savetxt
import time

filename = input('Filename (example: 2023-04.FIN):   ')
# filename = '2022-05.FIN'
ZONES = 2160
power = 8
scanning = False
dict_with_zones = {}
rel_powers = zeros((4, 4))
all_assemblies = ['F24', 'F55', 'F25', 'F22', 'F52', 'F44', 'F34', 'F32', 'F42', 'F53', 'F45', 'F33', 'F43', 'F54',
                  'F23', 'F35']
all_volumes = loadtxt('volumes.txt')
fa_cursor = 0
powers = zeros(2160)
sum_powers = 0
zone = 0
max_power = 0
max_fa_cursor = 0
with open(f'fins/{filename}', 'r') as fin_file:
    for line in fin_file:
        if line.find('MIXT') != -1:
            scanning = True
            # values in 2 lines after header with mixt, it's quicker with counter then check each line for values
            line_aftr_mixt = 0
            continue
        if scanning:
            if line_aftr_mixt != 1:
                line_aftr_mixt += 1
            else:
                powers[zone] = float(line.split()[1])
                line_aftr_mixt += 1
                if zone == 2159:
                    fa_power = sum(powers)
                    sum_powers += fa_power
                    powers = powers / all_volumes
                    if max(powers) > max_power:
                        max_power = max(powers)
                        argmax_fa = argmax(powers)
                        max_fa_cursor = fa_cursor
                    dict_with_zones[all_assemblies[fa_cursor]] = powers
                    rel_powers[
                        int(all_assemblies[fa_cursor][-2]) - 2, int(all_assemblies[fa_cursor][-1]) - 2] = fa_power
                    sector = (argmax_fa + 1) % 12
                    height = 60 - 2 * ((argmax_fa + 1) // 12) - 1
                    fuel_element = ((argmax_fa + 1) // 360) + 1
                    powers = zeros(2160)
                    fa_cursor += 1
                    zone = 0
                    if fa_cursor == 16:
                        break
                else:
                    zone += 1
koef_ = 1 / sum_powers * power * 1e6
rel_powers = (rel_powers / sum_powers * 100).T
print(
    f'most energy reliese in {all_assemblies[max_fa_cursor]}\npower={max_power * koef_:.2f}\nfuel_element:{fuel_element}\nsector:{sector}\nheight:{height}')
savetxt('absolute_fa_powers.txt', X=rel_powers, fmt='%.5e')
print('Absolute power distribution saved to absolute_fa_powers.txt')
height, cell = input(
    f'For radial distribution chose height and cell, for example for the most stressed cell: {height} {all_assemblies[max_fa_cursor][1:]}  :').split()
rad_distrib = zeros((6, 12))
chosen_height = 60 - int(height)
chosen_fa = 'F' + str(cell)
current_fe = 1
if chosen_height % 2 == 0:
    chosen_height += 1
for index_ in range(0, 2159, 360):
    start_index = int(((chosen_height + 1) / 2) * 12 - 12) + index_
    finish_index = start_index + 12
    rad_distrib[current_fe - 1:] = dict_with_zones[chosen_fa][start_index:finish_index]
    current_fe += 1
savetxt('relative_powers.txt', X=(rad_distrib / max(rad_distrib)), fmt='%.5e')
print('Relative power distribution saved to relative_fe_powers.txt')
input('Press any button and go fu** yourself')
print('Bye....')
time.sleep(1)
