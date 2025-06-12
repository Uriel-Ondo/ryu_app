from webob import Response
from ryu.app.wsgi import ControllerBase, route
from ryu.lib import ofctl_v1_3
import json

class SimpleFlowREST(ControllerBase):
    def __init__(self, req, link, data, **config):
        super(SimpleFlowREST, self).__init__(req, link, data, **config)
        self.app = data['app']

    @route('flows', '/flows', methods=['GET'])
    def list_flows(self, req, **kwargs):
        all_flows = {}
        for dpid, dp in self.app.datapaths.items():
            flows = ofctl_v1_3.get_flow(dp, {})
            all_flows[dpid] = flows
        return Response(content_type='application/json', body=json.dumps(all_flows))

    @route('flows', '/flows/add', methods=['POST'])
    def add_flow(self, req, **kwargs):
        body = json.loads(req.body)
        dpid = int(body.get("dpid"))
        flow = {
            "priority": int(body.get("priority")),
            "match": {
                "in_port": int(body.get("in_port")),
                "eth_src": body.get("eth_src"),
                "eth_dst": body.get("eth_dst")
            },
            "actions": [{"type": "OUTPUT", "port": int(body.get("out_port"))}]
        }
        ofctl_v1_3.mod_flow(self.app.datapaths[dpid], flow)
        return Response(status=200)

    @route('flows', '/flows/delete', methods=['POST'])
    def delete_flow(self, req, **kwargs):
        body = json.loads(req.body)
        dpid = int(body.get("dpid"))
        flow = {
            "priority": int(body.get("priority")),
            "match": {
                "in_port": int(body.get("in_port")),
                "eth_src": body.get("eth_src"),
                "eth_dst": body.get("eth_dst")
            }
        }
        ofctl_v1_3.delete_flow(self.app.datapaths[dpid], flow)
        return Response(status=200)
