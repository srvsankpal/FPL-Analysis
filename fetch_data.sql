USE `fpl`;
DROP procedure IF EXISTS `display_data`;

USE `fpl`;
DROP procedure IF EXISTS `fpl`.`display_data`;
;

DELIMITER $$
USE `fpl`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `display_data`(in total_points int, in avg_points float, in cost float, in form float, in fixture_difficulty float )
BEGIN

set @tot_pnts=ifnull(total_points,0);
set @avg_pnts= ifnull(avg_points,0) ;
set @cost=ifnull(cost,15);
set @form=ifnull(form,0);
set @fixt=ifnull(fixture_difficulty,5);


set @players="SELECT * FROM `fpl` where `Cost`<=? and `Total Points`>=? and `Points/Game`>=? and `Form (Last 3 Games Mean Points)`>=? and `Fixture Difficulty (Next 3)`<=? order by `Total Points` desc ";
prepare stmt from @players;
execute stmt using @cost, @tot_pnts, @avg_pnts, @form, @fixt;
deallocate prepare stmt;


END$$

DELIMITER ;
;

