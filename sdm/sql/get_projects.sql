select p.*,
(select count(*) from tasks where p_id=p.p_id) as p_tasks_count
from projects p
order by p.p_id