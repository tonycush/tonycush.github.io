var searching = window.location.search;
searching = searching.substring(1).split("%");
var this_company_number = searching[0];
var this_job_index = parseInt(searching[1]);
fetch("my_files/approved_results.json")
    .then(function (response) {
        if (!response.ok) {
            throw new Error("HTTP error, status = " + response.status);
        }
        return response.json();
    })
    .then(function (data) {
        console.log(this_company_number);
        console.log(this_job_index);
        this_comp_res = (data.filter(el => el.company_number === this_company_number))
        console.log(this_comp_res.length)
        if (this_comp_res.length > 0) {
            var accs_table_info = document.createElement('table');
            accs_table_info.className = "table table-striped";
            table_headings = "<strong><thead><tr><td>Year</td><td>Made to</td><td>Type</td><td>View</td></tr></thead></strong>";
            table_body = "<tbody>";
            for (i = 0; i < this_comp_res.length; i++) {
                //console.log(this_comp_res[i])
                table_body += "<tr><td>" + this_comp_res[i]['current_year'] + "</td>"
                table_body += "<td>" + this_comp_res[i]['made_up_to'] + "</td>"
                table_body += "<td>" + this_comp_res[i]['description'] + "</td>"
                if ('company_accounts' in this_comp_res[i]['taskAnswers']) {
                    table_body += "<td> <a href='accounts.html?" + this_company_number + "%" + this_comp_res[i]['job_index'] + "'>VIEW</a></td></tr>"
                } else {
                    table_body += "<td> NA </td></tr>"
                }
            }
            table_body += "</tbody>";
            accs_table_info.innerHTML += table_headings;
            accs_table_info.innerHTML += table_body;
            document.getElementById("accounts_info").appendChild(accs_table_info)

        } else {
            console.log("NOPE - NO ACCS RETRIEVED")
            var no_acc_message = document.createElement("div");
            no_acc_message.className = "container"
            no_acc_message.innerHTML = "NO ACCOUNTS AVAILABLE"
            document.getElementById("accounts_info").appendChild(no_acc_message)
        }

        console.log("*** FIRST HIT ***")
        console.log(data[0])
        console.log("*** THIS HIT ***")
        solo_acc_loc = (data.findIndex((item) => item.job_index === this_job_index));
        console.log(data[solo_acc_loc])
        console.log("*** THIS ACCOUNT ***")
        solo_acc_data = data[solo_acc_loc]['taskAnswers']['company_accounts']
        console.log(solo_acc_data)
        var accs_table = new Tabulator("#solo_accounts_table", {
            data: solo_acc_data, //assign data to table
            layout: "fitColumns", //fit columns to width of table (optional)
            columns: [
                { title: "row name", field: "acc_field" },
                { title: data[solo_acc_loc]['current_year'], field: "cy_l", hozAlign: "right", formatter: "money", formatterParams: {
                    symbol: "£",
                    precision: 0,
                } },
                { title: data[solo_acc_loc]['current_year'], field: "cy_r", hozAlign: "right", formatter: "money", formatterParams: {
                    symbol: "£",
                    precision: 0,
                } },
                { title: data[solo_acc_loc]['previous_year'], field: "py_l", hozAlign: "right", formatter: "money", formatterParams: {
                    symbol: "£",
                    precision: 0,
                } },
                {
                    title: data[solo_acc_loc]['previous_year'], field: "py_r", hozAlign: "right", formatter: "money", formatterParams: {
                        symbol: "£",
                        precision: 0,
                    }
                },                
                {
                    title: "R CHANGE", field: "r_change", hozAlign: "right", mutator: function(value,data){
                        value = data.cy_r - data.py_r
                        return value;
                    }, formatter: "money", formatterParams: {
                        symbol: "£",
                        precision: 0,
                    }
                },               
                {
                    title: "L CHANGE", field: "l_change", hozAlign: "right", mutator: function(value,data){
                        value = data.cy_l - data.py_l
                        return value;
                    }, formatter: "money", formatterParams: {
                        symbol: "£",
                        precision: 0,
                    }
                }
            ]
        });

        //Hide column that do not show any information
        var all_cols = accs_table.getColumns()
        for (i = 0; i < all_cols.length; i++) {
            cellage = (all_cols[i].getCells())
            console.log(cellage[i].getField())
            null_count = 0;
            for (j = 0; j < cellage.length; j++) {
                z = cellage[j].getValue()
                if (z == null) {
                    null_count += 1;
                } 
            }
            if (null_count == (cellage.length)) {
                console.log(all_cols[i].getField() + " contains all null values")
                accs_table.hideColumn(all_cols[i].getField())
            }
        }
    })