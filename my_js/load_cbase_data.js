var searching = window.location.search;
var this_company_number = searching.substring(1);
//this_company_name = this_company_name.split("%20").join(" ")

fetch("my_files/crunchbase_info_tidy.json")
    .then(function (response) {
        if (!response.ok) {
            throw new Error("HTTP error, status = " + response.status);
        }
        return response.json();
    })
    .then(function (mydata) {

        var this_company_pos = mydata.findIndex((item) => item.company_number === this_company_number);
        console.log(this_company_number)
        console.log(mydata[this_company_pos])
        //window.this_company_number = mydata[this_company_pos]['company_number']
        //console.log(this_company_number)
        var new_section = document.createElement('div');
        new_section.className = "comp_output";
        new_section.id = "comp_id";
        new_section.innerHTML = mydata[this_company_pos]['name'];
        document.getElementById("header").appendChild(new_section);

        var sec_keys = Object.keys(mydata[this_company_pos].sections[0]);
        for (var i = 0; i < mydata[this_company_pos].sections.length; i++) {
            var ori_name = mydata[this_company_pos].sections[i].name;
            var temp_name = ori_name.replace('<!---->', '')
            var updated = temp_name.trim();
            //console.log(ori_name)              
            if (updated != "null") {
                //console.log(updated);
                new_section = document.createElement('div');
                new_section.className = "comp_output";
                new_section.id = updated;
                new_section.innerHTML = '<strong>' + updated + '</strong>';
                document.getElementById("details").appendChild(new_section);

                for (var j = 0; j < sec_keys.length; j++) {
                    entry = sec_keys[j];
                    entry_type = typeof (mydata[this_company_pos].sections[i][entry]);
                    entry_length = mydata[this_company_pos].sections[i][entry].length;
                    if (entry_type == 'object' && entry_length > 0) {
                        switch (entry) {
                            case 'table':
                                section_table = document.createElement('table');
                                section_table.className = "table table-striped";
                                table_headings = "<strong><thead><tr>";
                                section_table_info = mydata[this_company_pos].sections[i][entry][0];
                                sect_table_len = section_table_info.columnNames.length;
                                for (var k = 0; k < sect_table_len; k++) {
                                    col_head = section_table_info.columnNames[k].trim();
                                    table_headings += "<th>" + col_head + "</th>"
                                }
                                table_headings += "</tr></thead></strong>";
                                table_body = "<tbody>";
                                sect_table_num_rows = section_table_info.rows.length;
                                for (var k = 0; k < sect_table_num_rows; k++) {
                                    table_body += "<tr>"
                                    row_details = section_table_info.rows[k];
                                    for (var l = 0; l < row_details[0].length; l++) {
                                        table_body += "<td>" + row_details[0][l] + "</td>"
                                    }
                                    table_body += "</tr>"
                                }
                                table_body += "</tbody>";
                                section_table.innerHTML += table_headings;
                                section_table.innerHTML += table_body;
                                document.getElementById(updated).appendChild(section_table);
                                break;
                            case 'imageCard':
                                image_count = (mydata[this_company_pos].sections[i][entry][0]["rows"].length)
                                image_keys = Object.keys(mydata[this_company_pos].sections[i][entry][0]["rows"][0]);
                                image_table = document.createElement('table');
                                image_table.className = "table table-striped";
                                image_table.innerHTML = "<strong><thead><tr><th>logo</th><th>Name</th><th>Info</th></tr></thead></strong>";
                                image_body = "<tbody>"
                                for (var k = 0; k < image_count; k++) {
                                    image_body += "<tr>";
                                    for (var l = 0; l < image_keys.length; l++) {
                                        this_image_key = image_keys[l]
                                        image_detail = mydata[this_company_pos].sections[i][entry][0]["rows"][k][this_image_key];
                                        image_body += "<td>" + image_detail + "</td>";
                                    }
                                    image_body += "</tr>";
                                }
                                image_body += "</tbody></div";
                                image_table.innerHTML += image_body;
                                document.getElementById(updated).appendChild(image_table);
                                break;
                            default:
                                for (var k = 0; k < entry_length; k++) {
                                    this_detail_keys = Object.keys(mydata[this_company_pos].sections[i][entry][k]);
                                    this_detail_values = Object.values(mydata[this_company_pos].sections[i][entry][k]);
                                    section_info = document.createElement('p');
                                    section_info.innerHTML = this_detail_keys + " ::: " + this_detail_values;
                                    document.getElementById(updated).appendChild(section_info);
                                }
                        }
                    }
                }
            }
        }
    })