# this script acts as a small bridge layer between the prov_risk model and whatever backend system needs the output

from prov_risk_inference import compute_prov_risk
import json

def prov_risk_bridge(text, incident_id):
    # run the provocation risk model on a given piece of text
    prov_value = compute_prov_risk(text)

    # build a simple record that ties the model output to an incident id
    record = {
        "incident_id": incident_id,
        "text": text,
        "prov_risk": prov_value
    }

    # return the record so it can be logged, sent to an API, or stored somewhere
    return record

# quick test example to make sure everything works
sample = prov_risk_bridge("Evacuate the mall, there’s an active shooter!", "INC_0001")

# pretty print the result as JSON so it’s easy to read
print(json.dumps(sample, indent=2))