# Copyright 2020 EMBL - European Bioinformatics Institute
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import re
import requests


def get_chromosome_number_for_accession(chromosome_accession, line_limit=100):
    ENA_TEXT_API_URL = "https://www.ebi.ac.uk/ena/browser/api/text/{0}?lineLimit={1}&annotationOnly=true"
    response = requests.get(ENA_TEXT_API_URL.format(chromosome_accession, line_limit))
    response_lines = response.content.decode("utf-8").split("\n")
    num_lines = len(response_lines)

    features_section_found, source_line_found = False, False
    chosen_response = []
    line_index = 0
    # Look for the "source" feature under the "Features" section in the text response
    while line_index < num_lines:
        line = response_lines[line_index]
        if not (features_section_found or line.lower().startswith("fh   key")):
            line_index += 1
            continue
        features_section_found = True
        # Based on "Data item positions" described here, http://www.insdc.org/files/feature_table.html#3.4.2
        # the sixth character represents the start of the feature key
        if not (source_line_found or line[5:].lower().startswith("source")):
            line_index += 1
            continue
        source_line_found = True
        if line[21:].startswith("/"):
            assembled_line = line.strip()
            line_index += 1
            # Assemble text spread across multiple lines until
            # we hit the next qualifier (starts with /) or the next section
            while line_index < num_lines and \
                    not (response_lines[line_index][21:].startswith("/")
                         or response_lines[line_index][5:6].strip() != ''):
                line = response_lines[line_index]
                assembled_line += " " + line[21:].strip()
                line_index += 1

            # Fall back to organelle in case of MT/Chloroplast accessions
            # and the reference notes in case of Linkage Group molecules
            chosen_response = re.findall('.*/chromosome=".+"', assembled_line) or \
                              re.findall('.*/organelle=".+"', assembled_line) or \
                              re.findall('.*/note=".+"', assembled_line)

            # If we have a response to give, no need to continue further
            # If the sixth character is not empty, we have reached the next feature, so no need to continue further
            if chosen_response or line[5:6].strip() != '':
                break
        else:
            line_index += 1

    if not chosen_response:
        return ""

    return str.split(chosen_response[0], '"')[1].strip()