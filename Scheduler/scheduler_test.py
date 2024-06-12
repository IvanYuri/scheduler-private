import json
import random
import sys


'''

second proposal for the general idea, using json file to
manage and store information. The code works if every shift can be
covered by all available staff for the right amount of days.

In this example, we have 3 shifts available for 6 days of the week,
for three staff members. Each staff member has 12 credits, or 12 shifts
to cover, filling out two shifts per staff per day.


.           .            .



The code randomly selects shifts for satff, meaning that
it will not distinguish seperate shifts from continuous ones,
that has to be changed accondingly to the need of each
user. maybe add some manual features (?)


My suggestion is that to improve the days of the week selection
while also improving the shifts selection, maybe use hours for shifts (?)
make more options to be adaptable to the company scheduling system.


'''
# Function to import the settings from the JSON file
def importSettings(settingsPath):
    with open(settingsPath) as f:
        data = json.load(f)
    return data

# Function to count the number of shifts available and needed to be covered
def countShift(settings):
    shiftsToFill = len(settings["spaces"]) * 3 * 6 # 3 shifts, 6 days a week
    numberOfStaff = len(settings["members"])
    shiftCoverable = numberOfStaff * 2 * 6

    # Check if there are enough staff members to cover all shifts
    if shiftsToFill > shiftCoverable:
        print(f"We are short staffed with {shiftsToFill} shifts to fill for {numberOfStaff} employees")
        sys.exit(1)
    print(f"We have {shiftsToFill} shifts to fill for {numberOfStaff} employees, able to cover {shiftCoverable} shifts")


def addStaffMember(settings, name, shifts):
    new_member = {"name": name, "shifts": shifts}
    settings["members"].append(new_member)

def addShift(settings, space_name, periods):
    new_shift = {"name": space_name, "period": periods}
    settings["spaces"].append(new_shift)

def saveSettings(settingsPath, data):
    with open(settingsPath, 'w') as f:
        json.dump(data, f, indent=4)
        
# Read the settings file path from command line arguments
settingsPath = sys.argv[1] # protect this
settings = importSettings(settingsPath)

countShift(settings)

# Print the staff members and their initial shifts
print(settings["members"])

# Define the days of the week and periods of the day
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
periods = ["Morning", "Afternoon", "Evening"]
shifts = []

# Set initial credits for each member
for member in settings["members"]:
    member["credit"] = 2

# Create a reference list of members to reset credits daily
referenceMembers = settings["members"]

# Loop through each day and assign shifts
for day in days:
    shifts.append({"Day" : day})
    # Reset credits for each member before starting a new day
    for member in referenceMembers:
        member["credit"] = 2
    
    day_shifts = shifts[-1]
    
    # Loop through each period and assign members to spaces
    for period in periods:
        success = len(settings["spaces"])
        while success > 0:
            memberAssigneds = random.sample(referenceMembers, len(settings["spaces"]))
            for space, member in zip(settings["spaces"], memberAssigneds):
                if member["name"] not in day_shifts:
                    day_shifts[member["name"]] = []
                if member["credit"] > 0:
                    day_shifts[member["name"]].append([period, space["name"]])
                    member["credit"] -= 1
                    success -= 1

# Print the final shift assignments
print(shifts)

def main():
    settingsPath = sys.argv[1]
    settings = importSettings(settingsPath)

    # Add new staff member from user input
    name = input("Enter the name of the new staff member: ")
    shifts = int(input(f"Enter the number of shifts for {name}: "))
    addStaffMember(settings, name, shifts)

    # Add new shift from user input
    space_name = input("Enter the name of the new space: ")
    periods = input("Enter the periods for the new space (comma-separated): ").split(',')
    addShift(settings, space_name, [period.strip() for period in periods])
    if name(input) == NULL:
        print("NO ADDITIONS")
        sys.exit(1)

    # Save the updated settings
    saveSettings(settingsPath, settings)

    print("Updated settings:")
    print(json.dumps(settings, indent=4))

if __name__ == "__main__":
    main()
