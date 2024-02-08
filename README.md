# sdm_todolist_django

A project demonstrating how to use [SQL DAL Maker](https://github.com/panedrone/sqldalmaker) + Python/ Django.

Front-end is written in Vue.js 2.7. RDBMS is SQLite3.

![demo-go.png](demo-go.png)

sdm.xml
```xml
<sdm>

    <dto-class name="dj-Project" ref="projects"/>

    <dto-class name="dj-ProjectLi" ref="get_projects.sql" pk="p_id"/>

    <dto-class name="dj-Task" ref="tasks"/>

    <dto-class name="dj-TaskLi" ref="tasks">
        <field column="t_comments" type="-"/>
    </dto-class>
    
    <dao-class name="_ProjectsDao">

        <crud dto="dj-Project">
            <create/>
            <read/>
            <delete/>
        </crud>

    </dao-class>

    <dao-class name="_TasksDao">

        <crud dto="dj-Task"/>

    </dao-class>

</sdm>
```
Generated code in action:
```go
class ProjectListView(APIView):
    def get(_):
        projects = dao_p.get_all_projects()
        sz = ProjectLiSerializer(projects, many=True)
        return Response(sz.data)
    
    def post(request):
        sz = ProjectSerializer(data=request.data)
        sz.is_valid(raise_exception=True)
        dao_p.create_project(sz)
        return HttpResponse(status=status.HTTP_201_CREATED)


class ProjectView(APIView):
    def get(_, p_id):
        project = dao_p.read_project(p_id)
        sz = ProjectSerializer(project)
        return Response(sz.data)
    
    def put(request, p_id):
        sz = ProjectSerializer(data=request.data, partial=True)
        sz.is_valid(raise_exception=True)
        dao_p.rename_project(p_id, sz.data['p_name'])
        return HttpResponse(status=status.HTTP_200_OK)
    
    def delete(_, p_id):
        _ds.delete_by_filter(Task, {'p_id': p_id})
        dao_p.delete_project(p_id)
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)
```
