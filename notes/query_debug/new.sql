        SELECT DISTINCT `tagging_tag`.id, `tagging_tag`.name, COUNT(`alibrary_release`.`id`)
        FROM
            `tagging_tag`
            INNER JOIN `tagging_taggeditem`
                ON `tagging_tag`.id = `tagging_taggeditem`.tag_id
            INNER JOIN `alibrary_release`
                ON `tagging_taggeditem`.object_id = `alibrary_release`.`id`
            %s
        WHERE `tagging_taggeditem`.content_type_id = 108
            %s
        GROUP BY `tagging_tag`.id, `tagging_tag`.name
        %s
        ORDER BY `tagging_tag`.name ASC