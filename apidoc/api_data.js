define({ "api": [
  {
    "type": "post",
    "url": "/task/add",
    "title": "Add Task",
    "version": "0.1.0",
    "group": "Task",
    "name": "Add_Task_to_database",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "type",
            "description": "<p>task type, 'USER' or 'SEARCH'</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "args",
            "description": "<p>task arguments</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "tittle",
            "description": "<p>task tittle</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"message\": \"success\",\n    \"status\": 200\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./restful/task.py",
    "groupTitle": "Task"
  },
  {
    "type": "post",
    "url": "/task/opt",
    "title": "Handle Task",
    "version": "0.1.0",
    "group": "Task",
    "name": "Handle_Task",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>task id</p>"
          },
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": "<p>operation on task, support &quot;stop&quot;, &quot;continue&quot;, &quot;drop&quot;</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"message\": \"success\",\n    \"status\": 200\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./restful/task.py",
    "groupTitle": "Task"
  },
  {
    "type": "get",
    "url": "/task/list",
    "title": "List Task",
    "version": "0.1.0",
    "group": "Task",
    "name": "List_task",
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "[\n  {\n    \"id\": 1,\n    \"tittle\": \"task A\",\n    \"type\": \"USER\",\n    \"status\": \"MONITOR\",\n    \"args\": \"realDonaldTrump\"\n  },\n  {\n    \"id\": 2,\n    \"tittle\": \"task B\",\n    \"type\": \"SEARCH\",\n    \"status\": \"MONITOR\",\n    \"args\": \"q=Donald Trump\"\n  }\n]",
          "type": "json"
        }
      ]
    },
    "filename": "./restful/task.py",
    "groupTitle": "Task"
  },
  {
    "type": "get",
    "url": "/task/status",
    "title": "Get Task Status",
    "version": "0.1.0",
    "group": "Task",
    "name": "Task_Status",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "Integer",
            "optional": false,
            "field": "id",
            "description": "<p>task id</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "\"MONITOR\"",
          "type": "json"
        }
      ]
    },
    "filename": "./restful/task.py",
    "groupTitle": "Task"
  },
  {
    "type": "get",
    "url": "/server/status",
    "title": "Get Crawler scheduler status",
    "version": "0.1.0",
    "group": "server",
    "name": "Crawler_scheduler_status",
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "\"runing\"",
          "type": "json"
        }
      ]
    },
    "filename": "./restful/server.py",
    "groupTitle": "server"
  },
  {
    "type": "post",
    "url": "/server/opt",
    "title": "server level operation",
    "version": "0.1.0",
    "group": "server",
    "name": "server_operation",
    "parameter": {
      "fields": {
        "Parameter": [
          {
            "group": "Parameter",
            "type": "String",
            "optional": false,
            "field": "cmd",
            "description": "<p>operation command, 'start' or 'stop', command equal status, no operating.</p>"
          }
        ]
      }
    },
    "success": {
      "examples": [
        {
          "title": "Success-Response:",
          "content": "{\n    \"message\": \"success\",\n    \"status\": 200\n}",
          "type": "json"
        }
      ]
    },
    "filename": "./restful/server.py",
    "groupTitle": "server"
  }
] });
