from pympesa import Pympesa
from pympesa import Pympesa, oauth_generate_token


def pay_cb2():
    response = oauth_generate_token(
        "w0sP3rGGfdTVDcpuAk4ADect3pFARVNU", "6hPJz5IEtxfv1X4E").json()
    access_token = response.get("access_token")

    mpesa_client = Pympesa(access_token)
    mpesa_client.c2b_register_url(
        ValidationUrl="https://us-central1-my-autoconnect.cloudfunctions.net/lmno_callback_url",
        ConfirmationUrl="https://us-central1-my-autoconnect.cloudfunctions.net/lmno_callback_url",
        ResponseType="Completed",
        ShortCode="174379"
    )

    mpesa_client.lipa_na_mpesa_online_payment(
        BusinessShortCode="174379",
        Password="bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919",
        TransactionType="CustomerPayBillOnline",
        Amount="100",
        PartyA="254796660187",
        PartyB="174379",
        PhoneNumber="254796660187",
        CallBackURL="https://us-central1-my-autoconnect.cloudfunctions.net/lmno_callback_url",
        AccountReference="ref-001",
        TransactionDesc="desc-001"
    )
