#!/usr/bin/env python3
"""Generate an author list for a new paper or abstract."""
import sys
from pathlib import Path
import json
from update_zenodo import get_git_lines, sort_contributors


# These authors should go last
AUTHORS_LAST = ['Gorgolewski, Krzysztof J.', 'Poldrack, Russell A.', 'Esteban, Oscar']


def _aslist(inlist):
    if not isinstance(inlist, list):
        return [inlist]
    return inlist


if __name__ == '__main__':
    devs = json.loads(Path('.maint/developers.json').read_text())
    contribs = json.loads(Path('.maint/contributors.json').read_text())

    author_matches, unmatched = sort_contributors(
        devs + contribs, get_git_lines(),
        exclude=json.loads(Path('.maint/former.json').read_text()),
        last=AUTHORS_LAST)
    # Remove position
    affiliations = []
    for item in author_matches:
        del item['position']
        for a in _aslist(item.get('affiliation', 'Unaffiliated')):
            if a not in affiliations:
                affiliations.append(a)

    aff_indexes = [', '.join(['%d' % (affiliations.index(a) + 1)
                              for a in _aslist(author.get('affiliation', 'Unaffiliated'))])
                   for author in author_matches]

    print("Some people made commits, but are missing in .maint/ "
          "files: %s." % ', '.join(unmatched), file=sys.stderr)

    print('Authors (%d):' % len(author_matches))
    print("%s." % '; '.join([
        '%s \\ :sup:`%s`\\ ' % (i['name'], idx)
        for i, idx in zip(author_matches, aff_indexes)
    ]))

    print('\n\nAffiliations:\n%s' % '\n'.join(['{0: >2}. {1}'.format(i + 1, a)
                                               for i, a in enumerate(affiliations)]))
