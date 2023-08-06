import pandas as pd
import pytest

from ovretl.performances_utils.calculate_shipments_treatment_steps_time import calculate_shipments_treatment_steps_time


@pytest.mark.skip(reason="Need to disable timezone")
def test_calculate_shipments_treatment_steps_time(snapshot):
    events_shipment_df = pd.read_csv("./ovretl/performances_utils/tests/events_shipment.csv")
    activities_clean_df = pd.read_csv("./ovretl/performances_utils/tests/activities_clean.csv")
    shipments_df = pd.read_csv("./ovretl/performances_utils/tests/shipments_df.csv")
    result = calculate_shipments_treatment_steps_time(
        events_shipment_df=events_shipment_df, activities_clean_df=activities_clean_df, shipments_df=shipments_df,
    )
    snapshot.assert_match(result)
