fetch("my_files/approved_results.json")
    .then(function (response) {
        if (!response.ok) {
            throw new Error("HTTP error, status = " + response.status);
        }
        return response.json();
    })
    .then(function (data) {            
        //console.log(this_company_number);
        this_comp_res = (data.filter(el => el.company_number === this_company_number))
        //console.log(this_comp_res.length)
        if (this_comp_res.length>0){
            var accs_table_info = document.createElement('table');
            accs_table_info.id = "turked_pdf";
            accs_table_info.className = "table table-striped";
            table_headings = "<strong><thead><tr><td>Year</td><td>Made to</td><td>Type</td><td>View</td></tr></thead></strong>";
            table_body = "<tbody>";
            for(i = 0 ; i < this_comp_res.length; i++){
                //console.log(this_comp_res[i])
                
                table_body += "<tr><td>"+ this_comp_res[i]['current_year']+"</td>"
                table_body += "<td>"+ this_comp_res[i]['made_up_to']+"</td>"
                table_body += "<td>"+ this_comp_res[i]['description']+"</td>"
                if('company_accounts' in this_comp_res[i]['taskAnswers']){
                    table_body += "<td> <a href='accounts.html?"+this_company_number+"%"+this_comp_res[i]['job_index'] +"'>VIEW</a></td></tr>"
                } else {
                    table_body += "<td> Not completed </td></tr>"
                }
            }
            table_body += "</tbody>";
            accs_table_info.innerHTML += table_headings;
            accs_table_info.innerHTML += table_body;
            document.getElementById("accounts_turked").appendChild(accs_table_info)

        } else {
            console.log("NOPE - NO ACCS RETRIEVED")
            var no_acc_message = document.createElement("div");
            no_acc_message.className = "container"
            no_acc_message.innerHTML= "NO ACCOUNTS AVAILABLE"
            document.getElementById("accounts_turked").appendChild(no_acc_message)
        }
        
    })