fetch("my_files/approved_results.json")
    .then(function (response) {
        if (!response.ok) {
            throw new Error("HTTP error, status = " + response.status);
        }
        return response.json();
    })
    .then(function (data) {
        console.log("RIGHT *** ACCESSING RESULTS")
        //console.log(this_company_name);
        //this_company_number = document.getElementById("comp_num");            
        console.log(this_company_number);
        //this_comp_res = data.filter(company_number => company_number === this_company_number);
        this_comp_res = (data.filter(el => el.company_number === this_company_number))
        console.log(this_comp_res.length)
        if (this_comp_res.length>0){
            for(i = 0 ; i < this_comp_res.length; i++){
                console.log(i)
                console.log(this_comp_res[i])
            }

        } else {
            console.log("NOPE - NO ACCS RETRIEVED")
        }
        
        var this_company_accs_pos = data.findIndex((item) => item.company_number === this_company_number);
        if (this_company_accs_pos != -1) {
            console.log("We gotta match")
            console.log(data[this_company_accs_pos])
            console.log(data[this_company_accs_pos]['company_name'])
        }

    })