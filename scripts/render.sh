#!/bin/sh
# omero login <USERNAME>@localhost -w<PASSWORD>

NOW=`date +%Y%m%d-%H%M%S`
mkdir "logs-render-$NOW"
function render {
    PROJECTNAME=idr0071-feldman-crisprko/experiment${1}
    echo $PROJECTNAME
    omero render batchset experiment${1}/renderdefs.yml > logs-render-$NOW/$1.out 2> logs-render-$NOW/$1.err
    echo "Finished $PROJECTNAME"
}

echo "Adding rendering settings in parallel in 5s"
sleep 5
for e in A B C D E F; do
    render $e &
done
