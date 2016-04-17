Trend_APP = {
   // 'selector_count':0,
    'trends':{},
    'render_selector' : function()
    {
        var article_types = [];
        var data = Trend_APP.trends
        for (var index in data){
            article_types.push(index);

        }
        var options='<option value="ALL">ALL</option>';
        for (index in article_types)
            {
                options = options + '<option value ="'+ article_types[index] + '">' + article_types[index] + '</option>'
            }
        var selector = '<select id="article_type_selector" class="form-control">' + options + '</select>'
        var selector_div = '<div class="col-sm-4"></div><div class="col-sm-4"><center>Select Article Type</center><br><center><form role="form"><div class="form-group">' + selector + '</div></form></center></div>'
        $('#selector').html(selector_div);
    },
    render_table:function(article_type)
    {

        if (article_type == 'ALL')
        {
            var rows=''
            for (category in Trend_APP['trends'])
            {
                var obj = Trend_APP['trends'][category];
                for (var trends in obj)
                {
                    rows = rows + '<tr><td>' + trends + '</td><td>' + obj[trends]['googlescore'].toFixed(2) + '</td><td>'+ obj[trends]['percentile'].toFixed(2)+ '</td><td>' + obj[trends]['itf_score'].toFixed(2) + '</td><td>' + obj[trends]['final_score'].toFixed(2) + '</td></tr>'
                }
            }
            var thead = '<thead> <tr> <th> Fashion Trends </th><th>Google Score <th> Percentile </th> <th> ITF Score </th><th> Final Score </th> </tr></thead>';
            var tbody='<tbody>' + rows + '</tbody>';
            var table = '<table  id="trends_table" class="table table-bordered table-striped">' + thead + tbody + '</table>';
            $('#graph_div').html('<br><center>' + table + '</center>');
            $('#trends_table').DataTable(
                {
                "scrollY":        "100%",
                "scrollCollapse": true,
                "paging":         false,
                "filter":false,
                "order": [[ 4, "desc" ]],
                "columnDefs": [
                            { "width": "30%", "targets": 0 },
                            { "bSortable": true, "aTargets":[1,2]}
                            ]
                });

            return;
        }
        $('#graph_div').html('<br><center>Loading Table ....</center>');

        var obj;
        for (category in Trend_APP.trends)
        {
            if( category == article_type )
            {
                obj = Trend_APP.trends[category];
                break;
            }
        }
        var thead = '<thead> <tr> <th> Fashion Trends </th><th>Google Score <th> Percentile </th> <th> ITF Score </th><th> Final Score </th> </tr></thead>';
        var rows=''
        for (trends in obj)
        {
            if (trends == undefined ){
            continue;
            }
           // var percentage_gap = (obj[type]['gap_count']*100/obj[type]['total_count']);
            rows = rows + '<tr><td>' + trends + '</td><td>' + obj[trends]['googlescore'].toFixed(2) + '</td><td>'+ obj[trends]['percentile'].toFixed(2) + '</td><td>' + obj[trends]['itf_score'].toFixed(2) + '</td><td>' + obj[trends]['final_score'].toFixed(2) + '</td></tr>'
        }
        var tbody='<tbody>' + rows + '</tbody>';
        var table = '<table  id="trends_table" class="table table-bordered table-striped">' + thead + tbody + '</table>';
        $('#graph_div').html('<br><center>' + table + '</center>');
        $('#trends_table').DataTable(
            {
            "scrollY":        "100%",
            "scrollCollapse": true,
            "paging":         false,
            "filter":false,
            "order": [[ 4, "desc" ]],
            "columnDefs": [
                        { "width": "30%", "targets": 0 },
                        { "bSortable": true, "aTargets":[1,2]}
                        ]
            });

    }
}
$(document).ready(function()
    {
        console.log('Document Loaded');
        $.ajax({
                    url: '/getTrending',
                    type: 'GET',
                    success: function(response)
                    {

                        Trend_APP.trends = JSON.parse(response)
                        Trend_APP.render_selector();
                        $('#article_type_selector').trigger('change');
                    },
                    error:function(){
                        console.log('Could not fetch selection gap data');
                    }
                })
    });

$(document).on('change', '#article_type_selector', function(event){
    console.log('Returned');
    console.log(event.target.value);
    Trend_APP.render_table(event.target.value);

});