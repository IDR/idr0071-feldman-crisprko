#!/bin/sh
# omero login <USERNAME>@localhost -w<PASSWORD>

echo "Deleting existing annotations in 5s"
sleep 5
for e in A B C D E F; do
    PROJECTNAME=idr0071-feldman-crisprko/experiment${e}
    echo $PROJECTNAME
    PROJECT=$(omero hql "FROM Project WHERE name='$PROJECTNAME'" --style plain --ids-only -q | cut -d, -f2)
    omero metadata populate --context deletemap --report --wait 300 --batch 1000 --localcfg '{"ns":["openmicroscopy.org/mapr/organism", "openmicroscopy.org/mapr/antibody", "openmicroscopy.org/mapr/gene", "openmicroscopy.org/mapr/cell_line", "openmicroscopy.org/mapr/phenotype", "openmicroscopy.org/mapr/sirna", "openmicroscopy.org/mapr/compound"], "typesToIgnore":["Annotation"]}' --cfg idr0071-bulkmap-config.yml $PROJECT
    omero metadata populate --context deletemap --report --wait 300 --batch 1000 --cfg idr0071-bulkmap-config.yml $PROJECT
    omero metadata deletebulkanns $PROJECT
done

echo "Adding bulk annotation tables in 5s"
sleep 5
for e in A B C D E F; do
    PROJECTNAME=idr0071-feldman-crisprko/experiment${e}
    echo $PROJECTNAME
    PROJECT=$(omero hql "FROM Project WHERE name='$PROJECTNAME'" --style plain --ids-only -q | cut -d, -f2)
    omero metadata populate --report --batch 1000 --file experiment${e}/idr0071-experiment${e}-annotation.csv $PROJECT
done

echo "Listing bulk annotation tables"
for e in A B C D E F; do
    PROJECTNAME=idr0071-feldman-crisprko/experiment${e}
    echo $PROJECTNAME
    PROJECT=$(omero hql "FROM Project WHERE name='$PROJECTNAME'" --style plain --ids-only -q | cut -d, -f2)
    omero metadata bulkanns --report $PROJECT
done

echo "Adding bulk map annotations in 5s"
sleep 5
for e in A B C D E F; do
    PROJECTNAME=idr0071-feldman-crisprko/experiment${e}
    BULKMAPCONFIG=idr0071-bulkmap-config.yml
    echo $PROJECTNAME
    PROJECT=$(omero hql "FROM Project WHERE name='$PROJECTNAME'" --style plain --ids-only -q | cut -d, -f2)
    omero metadata populate --context bulkmap --batch 1000 --cfg $BULKMAPCONFIG $PROJECT
done
