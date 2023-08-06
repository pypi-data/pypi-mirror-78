#
# Copyright (C) 2020 IHS Markit.
# All Rights Reserved
#
import os
from collections import OrderedDict
from typing import Dict

import requests

from dli.client.exceptions import CatalogueEntityNotFoundException
from dli.models.paginator import Paginator
from dli.client.components.urls import dataset_urls, identity_urls
from dli.models.dataset_model import DatasetModel
from dli.modules.package_module import PackageModule


class DatasetModule:

    def __call__(self, search_term=None, only_mine=False) \
            -> Dict[str, DatasetModel]:
        """
        See datasets.

        :param bool only_mine: Specify whether to collect datasets only
        accessible to you (True) or to discover packages that you may
        want to discover but may not have access to (False).

        :returns: Ordered dictionary of ids to DatasetModel.
        :rtype: OrderedDict[id: str, DatasetModel]
        """

        filters = {}
        for x in PackageModule._filter_creation(search_term, only_mine):
            filters.update(x)

        p = Paginator(
            dataset_urls.v2_index,
            self._client.Dataset,
            self._client.Dataset._from_v2_response_unsheathed,
            page_size=5000,
            max_workers=5,
            filters=filters
        )

        results = [(v.short_code, v) for v in p]
        o = OrderedDict()
        for code, val in results:
            if code in o:
                o[code] = [o[code]]
                o[code].append(val)
            else:
                o[code] = val

        return o

    def get(self, short_code, organisation_short_code=None) -> DatasetModel:
        """
        Returns a DatasetModel if it exists, and a user has access else None

        :param str short_code: The short code of the dataset to collect

        :returns: Dataset model with matching short code.
        :rtype: DatasetModel
        """

        search_terms = [
            f"short_code={short_code}"
        ]

        if organisation_short_code is not None:
            search_terms.append(
                f"organisation_short_code={organisation_short_code}"
            )

        visible_orgs = self._client.session.get(
            identity_urls.orgs_visible_to_user
        ).json()

        mapping_to_sc = dict(map(
            lambda x: (x["id"],
                       x["attributes"]["short_code"]
                       ),
             visible_orgs["data"])
        )

        # todo - not going to work as expected since the orderdict wont have dups
        res = self._client.datasets(search_term=search_terms, only_mine=False).get(short_code)

        if type(res) is list:
            if os.name != 'nt':
                org_codes=[f"\033[4m\033[92m\033[1morganisation_short_code=" \
                           f"{mapping_to_sc.get(x.organisation_id, x.organisation_id)}" \
                           f"\033[0;0m -> {x.short_code}"
                           for x in res]

                msg = f"\033[96mMultiple datasets have shortcode: \033[1m`{short_code}`\033[0;0m\n\nShortcodes are"\
                      f" only guaranteed to be unique per organisation, and you seem to "\
                      f" have access to multiple organisation's datasets, where there are "\
                      f"datasets bearing the same shortcode."\
                      f"\n"\
                      f"To resolve this, please specify the organisation_short_code in "\
                      f"the call to datasets.get(shortcode, organisation_short_code=ORG CODE)"\
                      f"\n\nThe available (accessible to you) organisations shortcodes "\
                      f"for this dataset short code are:\n" + ("\n".join(org_codes))
            else:
                org_codes = [f"organisation_short_code=" \
                             f"{mapping_to_sc.get(x.organisation_id, x.organisation_id)}" \
                             f" -> {x.short_code}"
                             for x in res]

                msg = f"Multiple datasets have shortcode: `{short_code}`\n\nShortcodes are" \
                      f" only guaranteed to be unique per organisation, and you seem to " \
                      f" have access to multiple organisation's datasets, where there are " \
                      f"datasets bearing the same shortcode." \
                      f"\n" \
                      f"To resolve this, please specify the organisation_short_code in " \
                      f"the call to datasets.get(shortcode, organisation_short_code=ORG CODE)" \
                      f"\n\nThe available (accessible to you) organisations shortcodes " \
                      f"for this dataset short code are:\n" + (
                          "\n".join(org_codes))


            raise Exception(
                msg
            )

            #todo - difficult here, really need to convert id to shortcode for org
            #todo - else isnt that useful a message as user now needs to discover these
        elif res:
            return res
        else:
            if self._client.strict:
                r = requests.Response()
                r.status_code = 404
                r.request = (lambda: True)
                r.request.method = f"No such dataset {short_code}"
                r.request.url = ""
                raise CatalogueEntityNotFoundException(
                    message=f"No such dataset {short_code}",
                    response=r
                )
            else:
                return None