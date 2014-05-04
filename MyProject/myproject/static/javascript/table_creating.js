function create_table()
{
    document.getElementById('relation_table').innerHTML = "<table id = 'tbl'></table>";
    var relations = find(company.departments, departmentName);
    var rel;
    for(rel in relations)
    {
        document.getElementById('tbl').innerHTML += "<tr> <td></td> <td></td> <td></td> </tr>";
    }
}