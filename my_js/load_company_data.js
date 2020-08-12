var searching = window.location.search;
var this_company_number = searching.substring(1);

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

        /*
        //adding iXBRL listing
        //console.log(mydata[this_company_pos]['ixbrl_info'])
        if (mydata[this_company_pos]['ixbrl_info'].length > 0) {
            var ixbrl_accs_table_info = document.createElement('table');
            ixbrl_accs_table_info.id = "ixbrl_table";
            ixbrl_accs_table_info.className = "table table-striped";
            table_headings = "<strong><thead><tr><td>Year</td><td>Made to</td><td>Type</td><td>View</td></tr></thead></strong>";
            table_body = "<tbody>";
            ixbrl_accs = mydata[this_company_pos]['ixbrl_info']
            for (ixbrl_file = 0; ixbrl_file < ixbrl_accs.length; ixbrl_file++) {

                ixbrl_accs[ixbrl_file][""]
                madeup = ixbrl_accs[ixbrl_file]["accs_made_up_to"]
                madeup_year = madeup.substring(madeup.length - 4, madeup.length)
                acc_type = ixbrl_accs[ixbrl_file]["accs_type"]
                //ixbrl_accs[ixbrl_file][""]
                table_body += '<tr><td>' + madeup_year + '</td><td>' + madeup + '</td><td>' + acc_type + '</td>\
                <td><button type="button" class="btn btn-primary" data-toggle="modal" data-target="#ixModal">\
                view</button></td></tr>'
                //Adding ixbrl account modal
                ix_accs_modal_ifo = '<div class="modal" id="ixModal">\
                <div class="modal-dialog">\
                    <div class="modal-content">\
                    <!-- Modal Header -->\
                    <div class="modal-header">\
                        <h4 class="modal-title">'+ madeup + '</h4>\
                        <button type="button" class="close" data-dismiss="modal">&times;</button>\
                    </div>\
                    <!-- Modal body -->\
                    <div class="modal-body">\
                       '+ixbrl_accs[ixbrl_file]["accs_table"]+'\
                    </div>\
                    <!-- Modal footer -->\
                    <div class="modal-footer">\
                        <button type="button" class="btn btn-danger" data-dismiss="modal">Close</button>\
                    </div>\
                    </div>\
                </div>\
                </div>';
            }
            table_body += "</tbody>";

            ixbrl_accs_table_info.innerHTML = table_headings + table_body + ix_accs_modal_ifo
        } else {
            var ixbrl_accs_table_info = document.createElement('p');
            ixbrl_accs_table_info.innerHTML = "This company has not filed any iXBRL files"
        }
        document.getElementById("accounts_ixbrl").appendChild(ixbrl_accs_table_info);
*/

        //Adding Company House Peoples
        var ch_people_output = document.createElement('div');
        ch_people_output.className = "container";
        ch_people_output.id = "ch-officers"
        ch_people_output_string = "<h6>Total Officers : <strong>" + mydata[this_company_pos]['company_house_people']['num_officers'] + "</strong></h6><h6>Total Resignations : <strong>" + mydata[this_company_pos]['company_house_people']['num_resignation'] + "</strong></h6><div class = 'container'>"
        ch_people_array = mydata[this_company_pos]['company_house_people']['officers'];
        for (i = 0; i < ch_people_array.length; i++) {
            officer_info = (Object.entries(ch_people_array[i]))
            //console.log(officer_info)
            //field = officer_info[0]
            //data = officer_info[1]

            ch_people_output_string += '<div class="card">\
            <div class="card-header"><h5>'+ ch_people_array[i]["Officer"] + '<h5>\
            <p>'+ ch_people_array[i]["Correspondence address"] + '</p></div>\
            <div class="card-body">\
                <div class="row">';
            //console.log(ch_people_array[i][4][0])
            for (info = 4; info < officer_info.length; info++) {
                //officer_detail = "JOHNO";
                //console.log(typeof(officer_info[info]))
                //console.log(officer_info[info])
                role_status = "";
                if (officer_info[info][0] == "Role") {
                    if (ch_people_array[i]["Status"] == "Active") {
                        btn_color = "btn-primary"
                    } else {
                        btn_color = "btn-secondary"
                    }
                    role_status = '<button type="button" class="btn btn-sm ' + btn_color + '" disabled>' + ch_people_array[i]["Status"] + '</button>';
                }
                ch_people_output_string += '<div class="col-sm-4">\
                    <p>'+ (officer_info[info][0]) + "  " + role_status + '</p>\
                    <p><strong>'+ (officer_info[info][1]) + '</strong></p>\
                    </div>';
            }

            ch_people_output_string += '</div>\
            </div>\
            <div class="card-footer"><p>'+ ch_people_array[i]["Officer link"] + '</p>\</div>\
        </div><br>';
        }
        ch_people_output_string += "</div>"
        ch_people_output.innerHTML = ch_people_output_string;
        document.getElementById("ch_people").appendChild(ch_people_output);

        //Adding Company House Overview Data
        var ch_overview_data = document.createElement('div');
        ch_overview_data.className = "container";
        ch_overview_data.id = "ch-over";
        ch_string = "<h6><strong>" + mydata[this_company_pos]['company_number'] + " : " + mydata[this_company_pos]['company_house_name'] + "</strong></h6>"
        ch_overview_data.innerHTML = ch_string;
        document.getElementById("ch_overview").appendChild(ch_overview_data);
        ch_overview_output = document.createElement('div')
        ch_overview_output.className = "row"

        var ch_overview = mydata[this_company_pos]['company_house_overview'];
        var ch_overview_keys = Object.keys(ch_overview);
        for (i = 0; i < ch_overview_keys.length; i++) {
            ch_overview_output_info = document.createElement('div');
            ch_overview_output_info.className = "col-md-6"
            //console.log(typeof(ch_overview[ch_overview_keys[i]]));
            ch_overview_title = ch_overview_keys[i].replace("_", " ")
            ch_overview_str = "<br><strong>" + ch_overview_title + "</strong>"
            if (ch_overview_title == "previous company_names") {
                ch_overview_str += "\
                <div class='container'>\
                    <table class='table table-striped'>\
                        <thead><th>Name</th><th>From</th><th>To</th></thead>\
                        <tbody>";
            }
            if (typeof (ch_overview[ch_overview_keys[i]]) == "string") {
                ch_overview_str += " : " + ch_overview[ch_overview_keys[i]]
            } else {
                for (j = 0; j < ch_overview[ch_overview_keys[i]].length; j++) {
                    if (typeof (ch_overview[ch_overview_keys[i]][j]) == "string") {
                        //console.log(ch_overview[ch_overview_keys[i]][j])
                        ch_overview_str += "<p>" + ch_overview[ch_overview_keys[i]][j] + "<\p>"
                    } else {
                        //looping through the array of dictionaries
                        ch_overview_output_info.className = "col-md-12"
                        ch_overview_subkeys = Object.keys(ch_overview[ch_overview_keys[i]][j])
                        if (ch_overview_subkeys.length == 1) {
                            for (k = 0; k < ch_overview_subkeys.length; k++) {
                                ch_overview_str += "<p><strong>" + ch_overview_subkeys[k] + "</strong> : " + ch_overview[ch_overview_keys[i]][j][ch_overview_subkeys[k]];
                            }
                        } else {
                            ch_overview_str += "<tr>";
                            for (k = 0; k < ch_overview_subkeys.length; k++) {
                                ch_overview_str += "<td>" + ch_overview[ch_overview_keys[i]][j][ch_overview_subkeys[k]] + "</td>";
                            }
                            ch_overview_str += "</tr>";
                            if (k == (ch_overview_subkeys.length - 1)) {
                                ch_overview_str += "</tbody></table>";
                            }
                        }
                    }
                }
            }
            ch_overview_output_info.innerHTML = ch_overview_str
            ch_overview_output.appendChild(ch_overview_output_info);
        }
        document.getElementById("ch-over").appendChild(ch_overview_output);

        //Adding Crunchbase data
        var cb_intro = document.createElement('div');
        cb_intro.className = "container";
        intro_string = "\
        <p><strong>Basic Info</strong>:   "+ mydata[this_company_pos]['basicInfo'] + "</p>\
        <p><strong>Description</strong>:  "+ mydata[this_company_pos]['description'] + "</p>\
        <p><strong>Location</strong>:     "+ mydata[this_company_pos]['location'] + "</p>";
        cb_intro.innerHTML = intro_string;
        document.getElementById("cb_intro").appendChild(cb_intro);

        var sec_keys = Object.keys(mydata[this_company_pos].sections[0]);
        for (var i = 0; i < mydata[this_company_pos].sections.length; i++) {
            var section_name = mydata[this_company_pos].sections[i].name;
            if (section_name != "null") {
                new_section = document.createElement('div');
                new_section.className = "cb_details_output container";
                new_section.id = section_name;
                new_section.innerHTML = '<strong>' + section_name + '</strong>';
                if (section_name == "Overview") {
                    document.getElementById("cb_overview").appendChild(new_section);
                } else {
                    document.getElementById("cb_details").appendChild(new_section);
                }
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
                                document.getElementById(section_name).appendChild(section_table);
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
                                document.getElementById(section_name).appendChild(image_table);
                                break;
                            default:
                                section_info = document.createElement('div');
                                section_info.className = "row"
                                for (var k = 0; k < entry_length; k++) {
                                    this_detail_keys = Object.keys(mydata[this_company_pos].sections[i][entry][k]);
                                    this_detail_values = Object.values(mydata[this_company_pos].sections[i][entry][k]);
                                    section_info_values = document.createElement('div');
                                    section_info_values.className = "col-md-6"
                                    section_info_values.innerHTML = this_detail_keys + " ::: " + this_detail_values;
                                    section_info.appendChild(section_info_values);
                                }
                                document.getElementById(section_name).appendChild(section_info);
                        }
                    }
                }
            }
        }
    })