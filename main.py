from fastapi import FastAPI
import secrets
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from numpy import size
from digion import digion
import uuid
import time
from fastapi.responses import FileResponse

app = FastAPI()
security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, "your-user")
    correct_password = secrets.compare_digest(credentials.password, "your-pass")
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

@app.get("/deploy_droplets")
async def read_item(project_name: str, workers: str,location: str ,user: str,service : str, username: str = Depends(get_current_username)):
    tag = str(uuid.uuid4()).replace('-', '')
    obj = digion()
    size_dict = {
        '1': 's-2vcpu-4gb',
        '2': 's-2vcpu-4gb',
        '3': 's-2vcpu-4gb',
        '4': 's-2vcpu-4gb',
        '5': 'g-2vcpu-8gb',
        '6': 'g-2vcpu-8gb',
        '7': 'g-2vcpu-8gb',
        '8': 'm-2vcpu-16gb',
        '9': 'm-2vcpu-16gb',
        '10': 'm-2vcpu-16gb',
    }
    location_dic = {
        'Newyork':'nyc1',
        'frank':'fra1',
        'london':'lon1',
        'Singapore':'sgp1',
        'Torento':'tor1',
        'san francisco':'sfo3',
        'bangalore':'blr1',
        'amsterdam':'ams3',
    }
    loc = location_dic.get(location)
    size = size_dict.get(workers)
    cre = obj.createvm(project_name, tag, size,loc)
    id_cloud = cre['id_cloud']
    date_at = cre['date']
    ip_cloud = obj.ip_address(id_cloud)
    service_dict = {
        'service_test_1': obj.ssh_doc,
        'service_test_1': obj.ssh_test,
    }
    func = service_dict.get(service)
    if ip_cloud == False:
        print('ip_address is False!!!')
    else:
        obj.insert(id_cloud, tag, ip_cloud, user, project_name, size, workers, date_at)
    time.sleep(30)
    func(ip_cloud)
    need = {
        "ip_address": ip_cloud + ':Your-port',
        "id_digion": id_cloud,
        "uuid": tag,
        "date": date_at,
        "workers": workers,
    }
    obj.uvicorn(ip_cloud, workers)
    return need


@app.get("/get_files")
async def read_item(file: str, username: str = Depends(get_current_username)):
    files_dic = {
        'file-test1': '/root/file1.zip',
        'file-test2': '/root/file2.zip',
    }
    file_get = files_dic.get(file)
    file_path = file_get
    return FileResponse(path=file_path, filename=file_path, media_type='zip,tar')

@app.get("/req_region")
async def read_item(username: str = Depends(get_current_username)):
    obj = digion()
    a = obj.req_region()
    return a

@app.get("/req_sizes")
async def read_item(username: str = Depends(get_current_username)):
    obj = digion()
    a = obj.req_sizes()
    return a

@app.get("/select_username")
async def read_item(user: str, username: str = Depends(get_current_username)):
    obj = digion()
    a = obj.select_username(user)
    return a

@app.get("/delete_droplets")
async def read_item(tag: str, username: str = Depends(get_current_username)):
    obj = digion()
    obj.delete(tag)
    need = {
        tag: "deleted " + tag
    }
    obj.delete_query(tag)
    return need


@app.get("/snapshot_droplets")
async def read_item(tag: str, nameshot: str, username: str = Depends(get_current_username)):
    obj = digion()
    obj.snapshot(tag, nameshot)
    need = {
        tag: "snapshot " + tag
    }
    return need


@app.get("/status_droplets")
async def read_item(tag: str, username: str = Depends(get_current_username)):
    obj = digion()
    obj.status(tag)
    return obj.status(tag)


@app.get("/reboot_droplets")
async def read_item(tag: str, username: str = Depends(get_current_username)):
    obj = digion()
    obj.reboot(tag)
    need = {
        tag: "rebooted " + tag
    }
    return need


@app.get("/poweroff_droplets")
async def read_item(tag: str, username: str = Depends(get_current_username)):
    obj = digion()
    obj.poweroff(tag)
    need = {
        tag: "poweroff " + tag
    }
    return need


@app.get("/poweron_droplets")
async def read_item(tag: str, username: str = Depends(get_current_username)):
    obj = digion()
    obj.poweron(tag)
    need = {
        tag: "poweron " + tag
    }
    return need 

