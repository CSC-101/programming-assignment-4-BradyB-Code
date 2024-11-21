import sys
import data
import build_data
import county_demographics
from typing import Optional

from data import CountyDemographics


# Task 1


def display(dataset: list[CountyDemographics])->None:
    for county in dataset:
        print("{}, {}".format(county.county, county.state))
        print("\tPopulation: {}".format(county.population["2014 Population"]))
        print("\tAge: ")
        for key in county.age.keys():
            print("\t\t{}: {}%".format(key, county.age[key]))

        print("\tEducation: ")
        for key in county.education.keys():
            print("\t\t{}: {}%".format(key, county.education[key]))

        print("\tEthnicity Percentages")
        for key in county.ethnicities.keys():
            print("\t\t{}: {}%".format(key, county.ethnicities[key]))

        print("\tIncome")
        for key in county.income.keys():
            print("\t\t{}: {}%".format(key, county.income[key]))




# main
demographics: list[CountyDemographics] = build_data.get_data()
if len(sys.argv) == 0:
    print("There are 0 arguments when 1 was expected")
    sys.exit()
file_name = sys.argv[1]

try:
        with open(sys.argv[1], "r") as operation:
            operation_contents: list[str] = operation.readlines()
            new_dataset = []

            for line_idx in range(len(operation_contents)):
                current_line = operation_contents[line_idx].strip("\n")
                operation_param: list[str] = current_line[line_idx].split(":")
                if line_idx == 0:
                    print(str(len(demographics)), " records loaded")

                if "filter-state" == operation_param[0]:
                    state = operation_param[1]
                    for county in demographics:
                        if county.state == state:
                            new_dataset.append(county)
                    print("Filter: state == ", state, "(", str(len(new_dataset)), "entries)")

                if "filter-gt" == operation_param[0]:
                    num = operation_param[2]
                    field = operation_param[1]
                    fields = field.split(".")
                    for county in demographics:
                        if fields[0] == "Education":
                            if county.education[fields[1]] > float(num):
                                new_dataset.append(county)
                        elif fields[0] == "Ethnicities":
                            if county.ethnicities[fields[1]] > float(num):
                                new_dataset.append(county)
                        elif fields[0] == "Income":
                            if county.income[fields[1]] > float(num):
                                new_dataset.append(county)
                        else:
                            print("Invalid field")
                    print("Filter: ", str(field), num, "(", str(len(new_dataset)), "entries)")

                if "filter-lt" == operation_param[0]:
                    num = operation_param[2]
                    field = operation_param[1]
                    fields = field.split(".")
                    for county in demographics:
                        if fields[0] == "Education":
                            if county.education[fields[1]] < float(num):
                                new_dataset.append(county)
                        elif fields[0] == "Ethnicities":
                            if county.ethnicities[fields[1]] < float(num):
                                new_dataset.append(county)
                        elif fields[0] == "Income":
                            if county.income[fields[1]] < float(num):
                                new_dataset.append(county)
                        else:
                            print("Invalid field")
                    print("Filter: ", str(field), num, "(", str(len(new_dataset)), "entries)")

                if "population-total" == current_line:
                    total = 0
                    if len(new_dataset) > 0:          #needs to also take the new_dataset
                        for county in new_dataset:
                            total += county.population["2014 Population"]
                    else:
                        for county in demographics:
                            total += county.population["2014 Population"]
                    print("2014 population: ", str(total))

                if "population" == operation_param[0]:
                    subpop = 0
                    field = operation_param[1]
                    fields = field.split(".")
                    if new_dataset:  # needs to also take the new_dataset
                        for county in new_dataset:
                            countypop = county.population["2014 Population"]
                            if fields[0] == "Education":
                                subpop += (countypop * county.education[fields[1]]) / 100
                            elif fields[0] == "Ethnicities":
                                subpop += (countypop * county.ethnicities[fields[1]]) / 100
                            elif fields[0] == "Income":
                                subpop += (countypop * county.income[fields[1]]) / 100
                            else:
                                print("Invalid field")

                    else:
                        for county in demographics:
                            countypop = county.population["2014 Population"]
                            if fields[0] == "Education":
                                subpop += (countypop * county.education[fields[1]]) / 100
                            elif fields[0] == "Ethnicities":
                                subpop += (countypop * county.ethnicities[fields[1]]) / 100
                            elif fields[0] == "Income":
                                subpop += (countypop * county.income[fields[1]]) / 100
                            else:
                                print("Invalid field")

                    print("2014", field, "population:", str(subpop))

                if "percent" == operation_param[0]:
                    subpop = 0
                    new_set_pop = 0
                    field = operation_param[1]
                    fields = field.split(".")
                    if new_dataset:
                        for county in new_dataset:
                            countypop = county.population["2014 Population"]
                            new_set_pop += countypop
                            if fields[0] == "Education":
                                subpop += (countypop * county.education[fields[1]]) / 100
                    print("2014", field, "percentage:", (subpop/new_set_pop))

                if "display" == current_line:
                    if new_dataset:
                        display(new_dataset)
                    else:
                        display(demographics)




except IOError as e:
    print("Error: ", e)

except IndexError as e:
    print("Error: ", e)




