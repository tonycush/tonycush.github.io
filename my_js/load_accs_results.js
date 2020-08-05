fetch('my_files/approved_results.json')
    .then(function (response) {
        if (!response.ok) {
            throw new Error('HTTP error, status = ' + response.status);
        }
        return response.json();
    })
    .then(function (data) {
        turk_data = data
        //console.log(this_company_number);
        this_comp_res = (data.filter(el => el.company_number === this_company_number))
        //console.log(this_comp_res.length)
        if (this_comp_res.length > 0) {
            var accs_table_info = document.createElement("table");
            accs_table_info.id = 'turked_pdf';
            accs_table_info.className = 'table table-striped';
            table_headings = '<strong><thead><tr><td>Year</td><td>Made to</td><td>Type</td><td></td></tr></thead></strong>';
            table_body = '<tbody>';
            for (i = 0; i < this_comp_res.length; i++) {
                //console.log(this_comp_res[i])
                //load_turk()
                table_body += '<tr><td>' + this_comp_res[i]["current_year"] + '</td>'
                table_body += '<td>' + this_comp_res[i]["made_up_to"] + '</td>'
                table_body += '<td>' + this_comp_res[i]["description"] + '</td>'
                if ("company_accounts" in this_comp_res[i]["taskAnswers"]) {
                    //table_body += '<td> <a href="accounts.html?'+this_company_number+'%'+this_comp_res[i]["job_index"] +'">VIEW</a></td></tr>'
                    table_body += '<td><button type="button" class="btn btn-primary turk_btn" value =' + this_comp_res[i]["job_index"] + '  id="' + this_comp_res[i]["job_index"] + '">View</button></td></tr>'
                } else {
                    table_body += '<td> Not completed </td></tr>'
                }
            }
            table_body += '</tbody>';
            accs_table_info.innerHTML += table_headings;
            accs_table_info.innerHTML += table_body;
            document.getElementById('accounts_turked').appendChild(accs_table_info)

        } else {
            console.log('NOPE - NO ACCS RETRIEVED')
            var no_acc_message = document.createElement('div');
            no_acc_message.className = 'container'
            no_acc_message.innerHTML = 'NO ACCOUNTS AVAILABLE'
            document.getElementById('accounts_turked').appendChild(no_acc_message)
        }

        $('.turk_btn').on('click', function (e) {
            this_job_index = parseInt(e.currentTarget.id)
            solo_acc_loc = (turk_data.findIndex((item) => item.job_index === this_job_index));
            //add the header
            turk_acc_title = '<h6><strong>' + turk_data[solo_acc_loc]['description'] + '</strong></h6>\
            <h6>'+ turk_data[solo_acc_loc]['made_up_to'] + '</h6>'
            document.getElementById('temp_output_title').innerHTML = turk_acc_title
            console.log("*** THIS ACCOUNT ***")
            console.log(turk_data[solo_acc_loc])


            solo_acc_data = turk_data[solo_acc_loc]['taskAnswers']['company_accounts']

            var accs_table = new Tabulator("#temp_output", {
                data: solo_acc_data, //assign data to table
                layout: "fitColumns", //fit columns to width of table (optional)
                headerSort: false,
                columns: [
                    { title: "", field: "acc_field" },
                    {
                        title: turk_data[solo_acc_loc]['current_year'], field: "cy_accounts", columns: [
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
                        title: turk_data[solo_acc_loc]['previous_year'], field: "cy_accounts", columns: [
                            {
                                title:"£", field: "py_l", hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                            {
                                title: "£", field: "py_r", hozAlign: "right", formatter: "money", formatterParams: {
                                    precision: 0,
                                }
                            },
                        ]
                    },{
                        title: "THE CHANGE", field: "changes", columns:[
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
                        ]},                    
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