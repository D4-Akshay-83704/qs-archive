[Abhayagiri library](photo:Abhayagiri library.jpg)
# Search instructions

The [search page](../search/Text-search.html) allows one to search excerpts for text, tags, and teachers. One can narrow the search to specific kinds of teaching or events. Simple queries are easy, but more complex searches require an understanding of how the search engine works. Read this page only as far as you need to and then start searching.

## Searching for text

To search for text, tags, or teachers, simply type the text into the search bar.

By default the search finds text within words. To find whole words only, enclose the word in double quotes. To find a phrase, enclose the phrase in double quotes.

For example, searching for `Thai` finds both Thai and Thailand, but searching for `"Thai"` finds only Thai.

## Searching for tags

Use brackets to search for excerpts tagged with specific tags:

Search for a single tag: `[Happiness]`

Search for all tags beginning with characters: `[History*]`

Search for all tags ending with characters: `[*Pasanno]`

Search for all tags containing characters: `[*Thai*]`

## Searching for teachers

Use braces to search for excerpts offered by specific teachers:

Search for a single teacher: `{Ajahn Dtun}`

Search for all teachers beginning with characters: `{Mae Chee*}`

Search for all teachers ending with characters: `{*Pasanno}`

## Searching by kind

To search for excerpts containing a specific kind of teaching, use a hash mark before or after the type of teaching:

Search for excepts containing a direct quote and the characters 'Thai': `#Quote Thai` 

Search for excepts containing an indirect quote and the characters 'Thai': `#IndirectQuote Thai`

Search for excepts containing both kinds of quotes and the characters 'Thai': `#*Quote Thai`

The available kinds are: `Question`, `Response`, `FollowUp`, `Story`, `Recollection`, `Teaching`, `Reflection`, `Simile`, `DhammaTalk`, `Quote`, `IndirectQuote`, `MeditationInstruction`, `GuidedMeditation`, `Chanting`, `Reading`, `Reference`, `Sutta`, `Vinaya`, `Comment`, `Discussion`, `Note`, `Summary`, `Other`, `Commentary`, `ReadBy`, and `TranslatedBy`.

## Searching by event

To search for excerpts from a specific event use the @ symbol before the event code. Event codes are of the form `Metta2008` or `UD2015-3` and contain a four-digit year. One can find event codes in the hyperlinks on the [Events page](../indexes/EventsBySeries.html). Since all events in a series begin with the same characters, one can search for excerpts from a particular series:

Search for Thanksgiving Retreats: `@TG`

Search for Winter Retreats: `@WR`

Search for Spirit Rock Daylongs: `@SRD`

Search for Upāsikā Days: `@UD`

Search for events from the year 2015: `@*2015`

## Advanced searching

To go beyond the recipies above, it is necessary to understand the search engine in  detail. The search engine converts excerpts and annotations into a series of blobs in which special characters are used to indicate tags, teachers, kinds, and events. For example, this excerpt:

![Example Excerpt](image:ExampleExcerpt.png)

is converted into these five blobs:

1. `#question#^could you please explain about the death process...how quickly does rebirth occur?^{ajahn pasanno}[death][rebirth][recollection/death][delusion][self-identity view][recollection][impermanence][not-self][theravada][history/early buddhism][sutta][vajrayana][clinging][culture/thailand][chanting][goodwill][relinquishment][ceremony/ritual][kamma]@metta2008@`
2. `#reference#^chanting book p 55: five recollections; chanting book p 12: the body is impermanent...^{}[similes][craving][rebirth]@metta2008@`
3. `#simile#^fire blown by the wind (mn-72: aggivacchagotta sutta)^{ajahn pasanno}[]@metta2008@`
4. `#story#^a former monk asks ajahn chah about working with dying people to give them the opportunity for wholesome rebirth.^{ajahn pasanno}[ajahn chah][death][teachers][rebirth][fierce/direct teaching]@metta2008@`
5. `#indirectquote#^i practice dying. the dalai lama^{ajahn pasanno}[dalai lama][recollection/death]@metta2008@`

The format of each blob can be informally represented as: `#kind#^text^{teachers}[tags]@eventCode@`.

Search queries are broken into individual strings separated by spaces. If all search strings can be found within an excerpts' blobs, then the excerpt is considered to be found.

The search engine implements the following wildcard characters:

`_` matches any single character except those with special meaning in the blobs: `#^[]{}@`

`*` matches any number of characters except those with special meaning

`$` matches a word boundary

Spaces divide individual search strings except for groups of characters enclosed in double quotes. Characters enclosed in double quotes only match word boundaries, but this can be changed using `*`. For example, `"Thai*"` and `$Thai` are equivalent queries.