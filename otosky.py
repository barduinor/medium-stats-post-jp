import argparse
import json
from datetime import datetime
from pathlib import Path

from medium_stats.scraper import StatGrabberPublication


def build_summary_stats_payload(publication_id: str):
    return {
        "operationName": "PublicationLifetimeStoryStatsPostsQuery",
        "variables": {
            "id": publication_id,
            # "first": 50,
            "first": 300,
            "after": "",
            "orderBy": {"publishedAt": "DESC"},
            "filter": {"published": True},
        },
        "query": """
    query PublicationLifetimeStoryStatsPostsQuery($id: String!, $first: Int!, $after: String!, $orderBy: PublicationPostsOrderBy, $filter: PublicationPostsFilter) {
      publication(id: $id) {
        id
        publicationPostsConnection(
          first: $first
          after: $after
          orderBy: $orderBy
          filter: $filter
        ) {
          __typename
          edges {
            ...PublicationLifetimeStoryStats_relayPublicationPostEdge
            __typename
          }
          pageInfo {
            endCursor
            hasNextPage
            __typename
          }
        }
        __typename
      }
    }
    fragment PublicationLifetimeStoryStats_relayPublicationPostEdge on RelayPublicationPostEdge {
      listedAt
      node {
        id
        ...LifetimeStoryStats_post
        __typename
      }
      __typename
    }
    fragment LifetimeStoryStats_post on Post {
      id
      ...StoryStatsTable_post
      ...MobileStoryStatsTable_post
      __typename
    }
    fragment StoryStatsTable_post on Post {
      ...StoryStatsTableRow_post
      __typename
      id
    }
    fragment StoryStatsTableRow_post on Post {
      id
      firstBoostedAt
      isLocked
      totalStats {
        views
        reads
        __typename
      }
      earnings {
        total {
          currencyCode
          nanos
          units
          __typename
        }
        __typename
      }
      ...TablePostInfos_post
      ...usePostStatsUrl_post
      __typename
    }
    fragment TablePostInfos_post on Post {
      id
      title
      readingTime
      isLocked
      visibility
      ...usePostUrl_post
      ...Star_post
      ...PostPreviewByLine_post
      __typename
    }
    fragment usePostUrl_post on Post {
      id
      creator {
        ...userUrl_user
        __typename
        id
      }
      collection {
        id
        domain
        slug
        __typename
      }
      isSeries
      mediumUrl
      sequence {
        slug
        __typename
      }
      uniqueSlug
      __typename
    }
    fragment userUrl_user on User {
      __typename
      id
      customDomainState {
        live {
          domain
          __typename
        }
        __typename
      }
      hasSubdomain
      username
    }
    fragment Star_post on Post {
      id
      creator {
        id
        __typename
      }
      __typename
    }
    fragment PostPreviewByLine_post on Post {
      id
      creator {
        ...PostPreviewByLine_user
        __typename
        id
      }
      collection {
        ...PostPreviewByLine_collection
        __typename
        id
      }
      ...CardByline_post
      __typename
    }
    fragment PostPreviewByLine_user on User {
      id
      __typename
      ...CardByline_user
      ...ExpandablePostByline_user
    }
    fragment CardByline_user on User {
      __typename
      id
      name
      username
      mediumMemberAt
      socialStats {
        followerCount
        __typename
      }
      ...useIsVerifiedBookAuthor_user
      ...userUrl_user
      ...UserMentionTooltip_user
    }
    fragment useIsVerifiedBookAuthor_user on User {
      verifications {
        isBookAuthor
        __typename
      }
      __typename
      id
    }
    fragment UserMentionTooltip_user on User {
      id
      name
      username
      bio
      imageId
      mediumMemberAt
      membership {
        tier
        __typename
        id
      }
      ...UserAvatar_user
      ...UserFollowButton_user
      ...useIsVerifiedBookAuthor_user
      __typename
    }
    fragment UserAvatar_user on User {
      __typename
      id
      imageId
      mediumMemberAt
      membership {
        tier
        __typename
        id
      }
      name
      username
      ...userUrl_user
    }
    fragment UserFollowButton_user on User {
      ...UserFollowButtonSignedIn_user
      ...UserFollowButtonSignedOut_user
      __typename
      id
    }
    fragment UserFollowButtonSignedIn_user on User {
      id
      name
      __typename
    }
    fragment UserFollowButtonSignedOut_user on User {
      id
      ...SusiClickable_user
      __typename
    }
    fragment SusiClickable_user on User {
      ...SusiContainer_user
      __typename
      id
    }
    fragment SusiContainer_user on User {
      ...SignInOptions_user
      ...SignUpOptions_user
      __typename
      id
    }
    fragment SignInOptions_user on User {
      id
      name
      __typename
    }
    fragment SignUpOptions_user on User {
      id
      name
      __typename
    }
    fragment ExpandablePostByline_user on User {
      __typename
      id
      name
      imageId
      ...userUrl_user
      ...useIsVerifiedBookAuthor_user
    }
    fragment PostPreviewByLine_collection on Collection {
      id
      __typename
      ...CardByline_collection
      ...CollectionLinkWithPopover_collection
    }
    fragment CardByline_collection on Collection {
      name
      ...collectionUrl_collection
      __typename
      id
    }
    fragment collectionUrl_collection on Collection {
      id
      domain
      slug
      __typename
    }
    fragment CollectionLinkWithPopover_collection on Collection {
      ...collectionUrl_collection
      ...CollectionTooltip_collection
      __typename
      id
    }
    fragment CollectionTooltip_collection on Collection {
      id
      name
      slug
      description
      subscriberCount
      customStyleSheet {
        header {
          backgroundImage {
            id
            __typename
          }
          __typename
        }
        __typename
        id
      }
      ...CollectionAvatar_collection
      ...CollectionFollowButton_collection
      __typename
    }
    fragment CollectionAvatar_collection on Collection {
      name
      avatar {
        id
        __typename
      }
      ...collectionUrl_collection
      __typename
      id
    }
    fragment CollectionFollowButton_collection on Collection {
      __typename
      id
      name
      slug
      ...collectionUrl_collection
      ...SusiClickable_collection
    }
    fragment SusiClickable_collection on Collection {
      ...SusiContainer_collection
      __typename
      id
    }
    fragment SusiContainer_collection on Collection {
      name
      ...SignInOptions_collection
      ...SignUpOptions_collection
      __typename
      id
    }
    fragment SignInOptions_collection on Collection {
      id
      name
      __typename
    }
    fragment SignUpOptions_collection on Collection {
      id
      name
      __typename
    }
    fragment CardByline_post on Post {
      ...DraftStatus_post
      ...Star_post
      ...shouldShowPublishedInStatus_post
      __typename
      id
    }
    fragment DraftStatus_post on Post {
      id
      pendingCollection {
        id
        creator {
          id
          __typename
        }
        ...BoldCollectionName_collection
        __typename
      }
      statusForCollection
      creator {
        id
        __typename
      }
      isPublished
      __typename
    }
    fragment BoldCollectionName_collection on Collection {
      id
      name
      __typename
    }
    fragment shouldShowPublishedInStatus_post on Post {
      statusForCollection
      isPublished
      __typename
      id
    }
    fragment usePostStatsUrl_post on Post {
      id
      creator {
        id
        username
        __typename
      }
      __typename
    }
    fragment MobileStoryStatsTable_post on Post {
      id
      firstBoostedAt
      isLocked
      totalStats {
        reads
        views
        __typename
      }
      earnings {
        total {
          currencyCode
          nanos
          units
          __typename
        }
        __typename
      }
      ...TablePostInfos_post
      ...usePostStatsUrl_post
      __typename
    }
    """,
    }


def get_article_ids(data: dict) -> list[str]:
    articles = data["data"]["publication"]["publicationPostsConnection"]["edges"]
    return [article["node"]["id"] for article in articles]


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument("--slug", required=True)
    parser.add_argument("--sid", required=True)
    parser.add_argument("--uid", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--stop", required=True)
    parser.add_argument("--output-dir", required=True)

    return parser


def write_json(data: dict, path: Path):
    json_str = json.dumps(data, indent=4)
    path.write_text(json_str)


def main():
    parser = create_parser()
    args = parser.parse_args()
    start = datetime.fromisoformat(args.start)
    stop = datetime.fromisoformat(args.stop)
    base_export_path = Path(args.output_dir) / "stats_exports" / args.slug
    base_export_path.mkdir(parents=True, exist_ok=True)

    pub = StatGrabberPublication(slug=args.slug, sid=args.sid, uid=args.uid, start=start, stop=stop)

    # get publication views & visitors (like the stats landing page)
    views = pub.get_events(type_="views")
    visitors = pub.get_events(type_="visitors")
    write_json(views, base_export_path / "views.json")
    write_json(visitors, base_export_path / "visitors.json")

    # get summary stats for all publication articles
    gql_endpoint = "https://medium.com/_/graphql"
    payload = build_summary_stats_payload(pub.id)
    response = pub.session.post(gql_endpoint, json=payload)
    response.raise_for_status()
    summary_stats = response.json()
    write_json(summary_stats, base_export_path / "summary_stats.json")

    # get individual article statistics
    articles = get_article_ids(summary_stats)
    article_events = pub.get_all_story_stats(articles)
    write_json(article_events, base_export_path / "article_events.json")

    referrers = pub.get_all_story_stats(articles, type_="referrer")
    write_json(referrers, base_export_path / "referrers.json")


if __name__ == "__main__":
    main()
