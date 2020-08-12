var searching = window.location.search;
var this_company_number = searching.substring(1);

fetch('my_files/crunchbase_info_tidy.json')
    .then(function (response) {
        if (!response.ok) {
            throw new Error('HTTP error, status = ' + response.status);
        }
        return response.json();
    })
    .then(function (filing_data) {

        var this_company_pos = filing_data.findIndex((item) => item.company_number === this_company_number);
        console.log(this_company_number)
        //console.log(filing_data[this_company_pos])
        //console.log(filing_data[this_company_pos]['filing_history'])

        //check if any accounts have been filed
        var first_aa_pos = filing_data[this_company_pos]['filing_history'].findIndex((item) => item.doc_code === "AA");
        if (first_aa_pos != -1) {
            var filing_history_table_info = document.createElement('table');
            filing_history_table_info.id = "filing_history_table";
            filing_history_table_info.className = "table table-striped";
            table_headings = "<strong><thead><tr><td>Year</td><td>Made to</td><td>Description</td><td>Type</td><td></td></tr></thead></strong>";
            table_body = "<tbody>";

            company_filing_history = filing_data[this_company_pos]['filing_history']
            ixbrl_accs = filing_data[this_company_pos]['ixbrl_info']
            
            turked_accs = filing_data[this_company_pos]['turked_answers']

            for (filed_acc = 0; filed_acc < company_filing_history.length; filed_acc++) {
                if (company_filing_history[filed_acc].doc_code == "AA") {
                    madeup = company_filing_history[filed_acc]["made_up_to"]
                    madeup_year = madeup.substring(madeup.length - 4, madeup.length)
                    acc_type = company_filing_history[filed_acc]["filing_desc"]
                    var this_ixblr_pos = ixbrl_accs.findIndex((item) => item.accs_made_up_to === madeup);
                    if (this_ixblr_pos >= 0) {
                        for (ans =0 ; ans<ixbrl_accs.length;ans++){
                            //console.log("%%% "+ixbrl_accs[ans]["accs_made_up_to"]+" %%%")
                            if(madeup == ixbrl_accs[ans]["accs_made_up_to"]){
                                if(ixbrl_accs[ans]["accs_table"]!= "Not parsed"){
                                    acc_link = 'iXBRL</td><td><button type="button" class="btn btn-primary ixbrl_btn" value =' + ans + ' id="' + ans + '">View</button>';
                                    break;
                                } else{
                                    acc_link = "iXBRL</td><td>Unparsed";
                                    break;
                                }
                                
                            } else{
                                acc_link = "iXBRL</td><td>WHO'S HERE"
                            }
                        }
                        
                        //acc_link = "iXBRL</td><td>IX FILE " + (this_ixblr_pos)
                    } else {
                        if ('turked_answers' in filing_data[this_company_pos]) {
                            var check_date = Date.parse(madeup)
                            for (ans = 0; ans < turked_accs.length; ans++) {
                                turk_file_date = Date.parse(turked_accs[ans]['made_up_to'])
                                if (check_date == turk_file_date) {
                                    if ("company_accounts" in turked_accs[ans]["taskAnswers"]){
                                        acc_link = 'pdf</td><td><button type="button" class="btn btn-primary turk_btn" value =' + turked_accs[ans]["job_index"] + '  id="' + turked_accs[ans]["job_index"] + '">View</button>';
                                        break;
                                    }else {
                                        acc_link = "pdf</td><td>No turk answers";
                                        break;
                                    }                                    
                                } else {
                                    acc_link = "pdf</td><td>Not processed";
                                }
                            }
                        } else {
                            acc_link = "pdf</td><td>Unanswered"
                        }
                    }
                    table_body += '<tr><td>' + madeup_year + '</td><td>' + madeup + '</td><td>' + acc_type + '</td>\
                    <td>' + acc_link + '</td></tr>';
                }
            }
            table_body += "</tbody>";

            filing_history_table_info.innerHTML = table_headings + table_body
        } else {
            var filing_history_table_info = document.createElement('p');
            filing_history_table_info.innerHTML = "This company has not filed any accounts"
        }
        document.getElementById("accounts_filed").appendChild(filing_history_table_info);

        //parsing info provided by scraping Companies House
        $('.ixbrl_btn').on('click', function (e){
            this_job_index = parseInt(e.currentTarget.id)

            solo_acc_data = ixbrl_accs[this_job_index]['accs_table']['data']

            //add the header
            ixbrl_acc_title = '<h6><strong>' + ixbrl_accs[this_job_index]['accs_type'] + '</strong></h6>\
            <h6>'+ ixbrl_accs[this_job_index]['accs_made_up_to'] + '</h6>'
            document.getElementById('temp_output_title').innerHTML = ixbrl_acc_title

            madeup = (ixbrl_accs[this_job_index]['accs_made_up_to'])
            madeup_year = parseInt( madeup.substring(madeup.length - 4, madeup.length))            

            //NEED TO CHECK WHAT THE COLUMN TITLES ARE...
            col_titles = ixbrl_accs[this_job_index]['accs_table']['schema']['fields']
            if(col_titles.length == 4){
                cy_r_var = col_titles[3]['name']
                cy_l_var = "cy_l"
                py_l_var = "py_l"
                py_r_var = "py_r"
            } else if (col_titles.length == 5) {
                last_col = col_titles[3]['name']
                last_col_char = last_col.substring(last_col.length-1,last_col.length)                
                
                if (last_col_char == '+'){   
                    //ONE YEAR TWO ACCOUNTS                 
                    cy_l_var = col_titles[3]['name']
                    cy_r_var = col_titles[4]['name']
                    py_l_var = "py_l"
                    py_r_var = "py_r"
                } else {
                    //TWO YEARS ONE COLUMN EACH
                    cy_r_var = col_titles[3]['name']
                    py_r_var = col_titles[4]['name']
                    cy_l_var = "cy_l"
                    py_l_var = "py_l"
                }

            } else {
                cy_l_var = col_titles[3]['name']
                cy_r_var = col_titles[4]['name']
                py_l_var = col_titles[5]['name']
                py_r_var = col_titles[6]['name']
            }
            var accs_table = new Tabulator("#temp_output", {
                data: solo_acc_data, //assign data to table
                layout: "fitColumns", //fit columns to width of table (optional)
                headerSort: false,
                columns: [
                    { title: "", field: "Title" },
                    {
                        title: madeup_year, field: "cy_accounts", columns: [
                            {
                                title: "£", field: cy_l_var, hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                            {
                                title: "£", field: cy_r_var, hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                        ]
                    },
                    {
                        title: madeup_year-1, field: "cy_accounts", columns: [
                            {
                                title: "£", field: py_l_var, hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                            {
                                title: "£", field: py_r_var, hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                        ]
                    }, {
                        title: "THE CHANGE", field: "changes", columns: [
                            {
                                title: "£", field: "l_change", hozAlign: "right", mutator: function (value, data) {
                                    return col_change(data[cy_l_var],data[py_l_var])
                                }, formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                            {
                                title: "£", field: "r_change", hozAlign: "right", mutator: function (value, data) {
                                    return col_change(data[cy_r_var],data[py_r_var])
                                     
                                }, formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            }
                        ]
                    },
                ]
            });
            var all_cols = accs_table.getColumns()
            for (i = 0; i < all_cols.length; i++) {
                cellage = (all_cols[i].getCells())
                null_count = 0;
                for (j = 0; j < cellage.length; j++) {
                    z = cellage[j].getValue()
                    if (z == null) {
                        null_count += 1;
                    }
                }
                if (null_count == (cellage.length)) {
                    accs_table.hideColumn(all_cols[i].getField())
                }
            }
            
            function col_change(current, previous){
                if (typeof (current && previous) == "string") {
                    current = check_for_negs(current)
                    previous = check_for_negs(previous)
                    value = current- previous
                    if (value == 0){
                        value = ""
                    }
                } else {
                    value = null
                }
                return value;
            }
            


        }) 

        function check_for_negs(val){
            if (val.charAt(0) == '('){
                temp = '-'+val.slice(1,-1)
                val = parseInt(temp)
            }
            return val
        }
        //parsing info provided by turkers
        $('.turk_btn').on('click', function (e) {
            this_job_index = parseInt(e.currentTarget.id)
            console.log(this_job_index)
            console.log(this_company_number)
            solo_acc_loc = (turked_accs.findIndex((item) => item.job_index === this_job_index));
            console.log(solo_acc_loc)
            //add the header
            turk_acc_title = '<h6><strong>' + turked_accs[solo_acc_loc]['description'] + '</strong></h6>\
            <h6>'+ turked_accs[solo_acc_loc]['made_up_to'] + '</h6>'
            document.getElementById('temp_output_title').innerHTML = turk_acc_title
            console.log("*** THIS ACCOUNT ***")
            console.log(turked_accs[solo_acc_loc])

            solo_acc_data = turked_accs[solo_acc_loc]['taskAnswers']['company_accounts']
            
            var accs_table = new Tabulator("#temp_output", {
                data: solo_acc_data, //assign data to table
                layout: "fitColumns", //fit columns to width of table (optional)
                headerSort: false,
                columns: [
                    { title: "", field: "acc_field" },
                    {
                        title: turked_accs[solo_acc_loc]['current_year'], field: "cy_accounts", columns: [
                            {
                                title: "£", field: "cy_l", hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                            {
                                title: "£", field: "cy_r", hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                        ]
                    },
                    {
                        title: turked_accs[solo_acc_loc]['previous_year'], field: "cy_accounts", columns: [
                            {
                                title: "£", field: "py_l", hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                            {
                                title: "£", field: "py_r", hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                        ]
                    }, {
                        title: "THE CHANGE", field: "changes", columns: [
                            {
                                title: "£", field: "l_change", hozAlign: "right", mutator: function (value, data) {
                                    if (typeof (data.cy_l && data.py_l) == "string") {
                                        value = data.cy_l - data.py_l
                                    } else {
                                        value = null
                                    }
                                    return value;
                                }, formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                            {
                                title: "£", field: "r_change", hozAlign: "right", mutator: function (value, data) {
                                    if (typeof (data.cy_r && data.py_r) == "string") {
                                        value = data.cy_r - data.py_r
                                    } else {
                                        value = null
                                    }
                                    return value;
                                }, formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            }
                        ]
                    },
                ]
            });
            //Hide column that do not show any information
            var all_cols = accs_table.getColumns()
            for (i = 0; i < all_cols.length; i++) {
                cellage = (all_cols[i].getCells())
                null_count = 0;
                for (j = 0; j < cellage.length; j++) {
                    z = cellage[j].getValue()
                    if (z == null) {
                        null_count += 1;
                    }
                }
                if (null_count == (cellage.length)) {
                    accs_table.hideColumn(all_cols[i].getField())
                }
            }
        });

    })