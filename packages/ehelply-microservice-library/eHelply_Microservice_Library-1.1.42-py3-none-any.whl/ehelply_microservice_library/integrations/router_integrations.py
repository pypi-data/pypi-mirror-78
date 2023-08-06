from starlette.requests import Request
from fastapi import Depends, Header, Query
from pydantic import BaseModel
from fastapi import HTTPException
from ehelply_microservice_library.utils.paginate import Paginator
from ehelply_microservice_library.utils.search_filter_sort import SQLSearch, SQLSort
from ehelply_bootstrapper.utils.cryptography import Hashing


def get_fact(request: Request):
    """
    Get fact service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_fact'):
        return request.state.i_fact
    else:
        raise Exception("Fact integration has not been registered")


def get_log(request: Request):
    """
    Get log service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_log'):
        return request.state.i_log
    else:
        raise Exception("Log integration has not been registered")


def get_note(request: Request):
    """
    Get note service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_note'):
        return request.state.i_note
    else:
        raise Exception("Note integration has not been registered")


def get_meta(request: Request):
    """
    Get meta service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_meta'):
        return request.state.i_meta
    else:
        raise Exception("Meta integration has not been registered")


def get_monitor(request: Request):
    """
    Get monitor service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_monitor'):
        return request.state.i_monitor
    else:
        raise Exception("Monitor integration has not been registered")


def get_user(request: Request):
    """
    Get user service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_user'):
        return request.state.i_user
    else:
        raise Exception("User integration has not been registered")


def get_access(request: Request):
    """
    Get access service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_access'):
        return request.state.i_access
    else:
        raise Exception("Access integration has not been registered")


def get_security(request: Request):
    """
    Get security service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_security'):
        return request.state.i_security
    else:
        raise Exception("Security integration has not been registered")


def get_m2m(request: Request):
    """
    Get M2M service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_m2m'):
        return request.state.i_m2m
    else:
        raise Exception("M2M integration has not been registered")


def get_appointments(request: Request):
    """
    Get appointments service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_appointments'):
        return request.state.i_appointments
    else:
        raise Exception("Appointments integration has not been registered")


def get_places(request: Request):
    """
    Get places service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_places'):
        return request.state.i_places
    else:
        raise Exception("Places integration has not been registered")


def get_reviews(request: Request):
    """
    Get reviews service integration
    :param request:
    :return:
    """
    if hasattr(request.state, 'i_reviews'):
        return request.state.i_reviews
    else:
        raise Exception("Reviews integration has not been registered")


class Integrations:
    """
    Common integrations
    """

    def __init__(
            self,
            fact,
            log,
            note,
            meta,
            monitor,
            user,
            access,
            security,
            m2m,
            appointments,
            places,
            reviews,
    ) -> None:
        super().__init__()

        self.fact = fact
        self.log = log
        self.note = note
        self.meta = meta
        self.monitor = monitor
        self.user = user
        self.access = access
        self.security = security
        self.m2m = m2m
        self.appointments = appointments
        self.places = places
        self.reviews = reviews


def get_integrations(
        request: Request
) -> Integrations:
    """
    Dependency injection helper to get all integrations if you're lazy like me and don't want to specify a laundry list
      each time.
    Marginally lower performance on each endpoint this is used. If really trying to optimize common endpoints,
      don't use this.
    :param request:
    :return:
    """
    try:
        fact = get_fact(request=request)
    except:
        fact = None

    try:
        log = get_log(request=request)
    except:
        log = None

    try:
        note = get_note(request=request)
    except:
        note = None

    try:
        meta = get_meta(request=request)
    except:
        meta = None

    try:
        monitor = get_monitor(request=request)
    except:
        monitor = None

    try:
        user = get_user(request=request)
    except:
        user = None

    try:
        access = get_access(request=request)
    except:
        access = None

    try:
        security = get_security(request=request)
    except:
        security = None

    try:
        m2m = get_m2m(request=request)
    except:
        m2m = None

    try:
        appointments = get_appointments(request=request)
    except:
        appointments = None

    try:
        places = get_places(request=request)
    except:
        places = None

    try:
        reviews = get_reviews(request=request)
    except:
        reviews = None

    return Integrations(
        fact=fact,
        log=log,
        note=note,
        meta=meta,
        monitor=monitor,
        user=user,
        access=access,
        security=security,
        m2m=m2m,
        appointments=appointments,
        places=places,
        reviews=reviews,
    )


def get_auth(
        request: Request,
        x_access_token: str = Header(None),
        x_secret_token: str = Header(None),
        authorization: str = Header(None),
        ehelply_active_participant: str = Header(None)
):
    """
    Helpful dependency injection
    :param access:
    :param user:
    :param access_token:
    :param secret_token:
    :param entity_uuid:
    :param entity_type:
    :return:
    """
    from ehelply_microservice_library.integrations.access import Auth
    from ehelply_microservice_library.integrations.m2m import M2M
    my_auth = Auth(access=get_access(request=request))
    m2m = get_m2m(request=request)

    if authorization:
        try:
            claims = m2m.verify_token(token=authorization)
        except:
            raise HTTPException(status_code=401, detail="Unauthenticated - Denied by eHelply")

        if ehelply_active_participant:
            if ehelply_active_participant in claims['custom:participants'].split(','):
                my_auth.entity_uuid = ehelply_active_participant
            else:
                raise HTTPException(status_code=401, detail="Invalid active participant - Denied by eHelply")

        my_auth.claims = claims

    if x_secret_token and x_access_token:
        my_auth.access_token = x_access_token
        my_auth.secret_token = x_secret_token
        my_auth.entity_type = "bot"

    return my_auth


def get_pagination(
        request: Request,
        page: int = Query(1),
        page_size: int = Query(25),
):
    """
    Returns an instance of pagination which can be used with a query
    :param request:
    :param page:
    :param page_size:
    :return:
    """
    return Paginator(page=page, page_size=page_size)


def get_search(
        request: Request,
        search: str = Query(None),
        search_on: str = Query(None)
):
    """
    Returns a query with a search applied.

    Args:
        request:
        search:
        search_on:

    Returns:

    """
    if search and len(search) < 3:
        raise HTTPException(status_code=400,
                            detail="Search criteria must be at least 3 characters long - Denied by eHelply")

    return SQLSearch(search_text=search, column=search_on)


def get_sort(
        request: Request,
        sort_on: str = Query(None),
        sort_desc: bool = Query(False),
):
    """
    Returns a query with a sort applied
    Args:
        request:
        sort_on:
        sort_desc:

    Returns:

    """
    return SQLSort(column=sort_on, desc=sort_desc)
