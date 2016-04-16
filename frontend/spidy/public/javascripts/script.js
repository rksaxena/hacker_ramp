SPIDY_APP = {
   // 'selector_count':0,
    'selection_gap':[],
    'render_selector' : function()
    {
        var sources = [];
        var data = SPIDY_APP.selection_gap
        for (var index in data){
            sources.push(data[index]['source'])

        }
        var options = '<option value="ALL" >ALL</option>'
        for (index in sources)
            {
                options = options + '<option value ="'+ sources[index] + '">' + sources[index] + '</option>'
            }
        var selector = '<select id="source_selector" class="form-control">' + options + '</select>'
        var selector_div = '<div class="col-sm-4"></div><div class="col-sm-4"><center>Select Source</center><br><center><form role="form"><div class="form-group">' + selector + '</div></form></center></div>'
        $('#selector').html(selector_div);




    },
    render_table:function(source)
    {

        $('#graph_div').html('<br><center>Loading Table ....</center>');
        if (source == 'ALL')
        {
            var master_object={}
            for (var index in SPIDY_APP.selection_gap)
            {
                var obj = SPIDY_APP.selection_gap[index];
                for (type in obj)
                {
                    if (type == 'source')
                    {
                        continue;
                    }
                    if (type in master_object)
                    {
                        for (var i in obj[type]['absent_trends'])
                        {
                            if (master_object[type].indexOf(obj[type]['absent_trends'][i]) > 0)
                                {
                                    continue;
                                }
                            master_object[type].push(obj[type]['absent_trends'][i]);
                        }
                    }
                    else
                    {
                        master_object[type]=obj[type]['absent_trends'];
                    }
                }
            }
            var thead = '<thead> <tr> <th> Categories </th> <th> Missing Fashion Objects </th> </tr></thead>';
            var rows = '';
            for (type in master_object)
            {
                if (type == undefined ){
                continue;
                }
               // var percentage_gap = (obj[type]['gap_count']*100/obj[type]['total_count']);
                rows = rows + '<tr><td>' + type + '</td><td>' + master_object[type] + '</td></tr>'
            }
            var tbody='<tbody>' + rows + '</tbody>';
            var table = '<table class="table table-bordered table-striped">' + thead + tbody + '</table>';
            $('#graph_div').html('<br><center>' + table + '</center>');
            return ;
        }
        var obj;
        for (index in SPIDY_APP.selection_gap)
        {
            if( SPIDY_APP.selection_gap[index]['source'] == source )
            {
                obj = SPIDY_APP.selection_gap[index];
                break;
            }
        }
        var thead = '<thead> <tr> <th> Categories </th> <th> Missing Fashion Objects </th> </tr></thead>';
        var rows=''
        for (type in obj)
        {
            if (type == undefined || type =='source'){
            continue;
            }
           // var percentage_gap = (obj[type]['gap_count']*100/obj[type]['total_count']);
            rows = rows + '<tr><td>' + type + '</td><td>' + obj[type]['absent_trends'] + '</td></tr>'
        }
        var tbody='<tbody>' + rows + '</tbody>';
        var table = '<table class="table table-bordered table-striped">' + thead + tbody + '</table>';
        $('#graph_div').html('<br><center>' + table + '</center>');
    }
}
$(document).ready(function()
    {
        console.log('Document Loaded');
        $.ajax({
                    url: '/getSelectionGap',
                    type: 'GET',
                    success: function(response)
                    {

                        SPIDY_APP.selection_gap = JSON.parse(response)['data']
                        SPIDY_APP.render_selector();
                        $('#source_selector').trigger('change');
                    },
                    error:function(){
                        console.log('Could not fetch selection gap data');
                    }
                })
    });

$(document).on('change', '#source_selector', function(event){
    console.log('Returned');
    console.log(event.target.value);
    SPIDY_APP.render_table(event.target.value);
})