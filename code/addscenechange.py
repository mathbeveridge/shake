import updatescript as update

# Adds a clear demarcation at the start of each scene change that will be used
# during scene analysis
#


# This standardizes scene transitions, which are marked by INT. EXT. and CUT TO.

#
# file_name_prefix_list = [
#     "/mac/NarrativeEcosystem/script/season5/data/s5e01",
#     "/mac/NarrativeEcosystem/script/season5/data/s5e02",
#     "/mac/NarrativeEcosystem/script/season5/data/s5e03",
#     "/mac/NarrativeEcosystem/script/season5/data/s5e04",
#     "/mac/NarrativeEcosystem/script/season5/data/s5e05",
#     "/mac/NarrativeEcosystem/script/season5/data/s5e06",
#     "/mac/NarrativeEcosystem/script/season5/data/s5e07",
#     "/mac/NarrativeEcosystem/script/season5/data/s5e08",
#     "/mac/NarrativeEcosystem/script/season5/data/s5e09",
#     "/mac/NarrativeEcosystem/script/season5/data/s5e10",
#      ]


file_name_prefix_list = [
     "/mac/NarrativeEcosystem/script/season7/data/s7e01",
]

input_suffix = ".tex"
output_suffix = "v2.tex"

for file_name_prefix in file_name_prefix_list:
    scriptlines = update.get_script(file_name_prefix + input_suffix)

    with open(file_name_prefix + output_suffix, 'w') as f:
        print(len(scriptlines))



        for line in scriptlines:
            line = line.strip()
            if line.startswith("EXT.") or line.startswith("INT.") or line.startswith("CUT TO:"):
                f.write("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -\n[")
                f.write(line)
                f.write("]\n")
            else:
                print(f)
                f.write(line)
                f.write("\n")

        f.close()

