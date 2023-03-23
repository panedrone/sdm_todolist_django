# sdm_demo_todolist_django
Quick Demo of how to use [SQL DAL Maker](https://github.com/panedrone/sqldalmaker) + Python + Django.

Front-end is written in Vue.js, SQLite3 is used as database.

![demo-go.png](demo-go.png)

dto.xml
```xml
<dto-class name="dj-Project" ref="projects"/>

<dto-class name="dj-ProjectLI" ref="get_projects.sql" pk="p_id"/>

<dto-class name="dj-Task" ref="tasks"/>

<dto-class name="dj-TaskLI" ref="tasks">
    <header><![CDATA[
    # Task list item. No no t_comments.]]></header>
    <field column="t_comments" type="-"/>
</dto-class>
```
ProjectsDao.xml
```xml
<crud dto="dj-Project" table="projects"/>

<query-dto-list dto="dj-ProjectLI" method="get_projects"/>
```
TasksDao.xml
```xml
<crud dto="dj-Task" table="tasks"/>
```
Generated code in action:
```go
class ProjectListView(APIView):
    @staticmethod
    def get(_):
        projects = dao.get_all_projects()
        sz = ProjectLISerializer(projects, many=True)
        return Response(sz.data)
    
    @staticmethod
    def post(request):
        sz = ProjectEditSerializer(data=request.data)
        sz.is_valid(raise_exception=True)
        dao.create_project(sz)
        return HttpResponse(status=status.HTTP_201_CREATED)


class ProjectView(APIView):
    @staticmethod
    def get(_, p_id):
        gr = dao.read_project(p_id)
        sz = ProjectSerializer(gr, many=False)
        return Response(sz.data)
    
    @staticmethod
    def put(request, p_id):
        sz = ProjectEditSerializer(data=request.data, partial=True)
        sz.is_valid(raise_exception=True)
        dao.rename_project(p_id, sz.data['p_name'])
        return HttpResponse(status=status.HTTP_200_OK)
    
    @staticmethod
    def delete(_, p_id):
        _ds.delete_by_filter(Task, {'p_id': p_id})
        dao.delete_project(p_id)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
```