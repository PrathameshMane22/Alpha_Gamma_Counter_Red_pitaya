    # Alpha Gamma Counter
    # Copyright (C) 2025 Prathamesh Mane
    
    # This program is free software: you can redistribute it and/or modify it
    # It is under the terms of the GNU General Public License as published by
    # the Free Software Foundation, either version 3 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License
    # along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pandas as pd

# Load the CSV file
df = pd.read_csv("C:/Users/catar/Prathamesh/June_Work/17-06-2025/data_csv.csv")

# Function to compute time difference ignoring zeroes
def compute_time_diff(series):
    diffs = []
    prev = None
    for value in series:
        if value == 0:
            diffs.append("-")
        else:
            if prev is None:
                diffs.append("-")
            else:
                diffs.append(round(value - prev, 6))
            prev = value
    return diffs

# Compute time differences
df["time_diff_alpha"] = compute_time_diff(df["time_alpha"])
df["time_diff_gamma"] = compute_time_diff(df["time_gamma"])

# Save the updated DataFrame to an Excel file
df.to_excel("C:/Users/catar/Prathamesh/June_Work/17-06-2025/output_with_time_diff.xlsx", index=False)
