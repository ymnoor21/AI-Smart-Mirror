/* Magic Mirror Config Sample
/* Magic Mirror Config Sample
 *
 * By Michael Teeuw http://michaelteeuw.nl
 * MIT Licensed.
 */

var config = {
	port: 8080,

	language: 'en',
	timeFormat: 24,
	units: 'imperial',

	modules: [
        {
            module: 'aiclient',
            position: 'middle_center' // This can be any of the regions.
        },
        {
        	module: 'aiclientdebugger',
        	position: 'bottom_right'
        },
        {
            module: 'clock',
            position: 'top_left',
            config: {
                'displayType': 'both',
                'analogSize': '200px',
                'analogFace': 'face-005',
                'secondsColor': '#ffffff'
            }
        },
        {
            module: 'calendar',
            header: 'VIEDU Programmers',
            position: 'top_left',
            config: {
                calendars: [
                    {
                        'symbol': 'calendar',
                        'url': 'https://calendar.google.com/calendar/ical/viedu.org_6j9lp4jo72uaife6s3iu3o53k8%40group.calendar.google.com/public/basic.ics'
                    }
                ]
            }
        },
        {
            module: 'calendar',
            header: 'My Calendar',
            position: 'top_left',
            config: {
                calendars: [
                    {
                        'symbol': 'calendar',
                        'url': 'https://calendar.google.com/calendar/ical/ymnoor21%40gmail.com/private-c4126a04bb38426c23ccb2c6a875fb80/basic.ics'
                    }
                ]
            }
        },
        {
            module: 'calendar',
            header: 'US Holidays',
            position: 'top_left',
            config: {
                calendars: [
                    {
                        symbol: 'calendar',
                        url: 'webcal://www.calendarlabs.com/templates/ical/US-Holidays.ics'
                    }
                ]
            }
        },
        {
            module: 'currentweather',
            position: 'top_right',
            config: {
                location: 'Folsom, CA',
                locationID: '',  //ID from http://www.openweathermap.org
                appid: 'e15ca5d4d80c3a45e4de2028bd640a13'
            }
        },
        {
            module: 'weatherforecast',
            position: 'top_right',
            header: 'Weather Forecast',
            config: {
                        location: 'Folsom, CA',
                locationID: '',  //ID from http://www.openweathermap.org
                        appid: 'e15ca5d4d80c3a45e4de2028bd640a13'
            }
        },
        {
            module: 'newsfeed',
            position: 'bottom_bar',
            config: {
                feeds: [
                    {
                        title: "Prothom Alo",
                        url: "http://www.prothom-alo.com/feed/",
                        encoding: 'utf-8'
                    }
                ],
                showSourceTitle: true,
                showPublishDate: true
            }
        },
        {
            module: 'newsfeed',
            position: 'bottom_bar',
            config: {
                feeds: [
                    {
                        title: "The Daily Star",
                        url: "http://www.thedailystar.net/latest/rss/rss.xml"
                    }
                ],
                showSourceTitle: true,
                showPublishDate: true
            }
        },
        {
            module: 'newsfeed',
            position: 'bottom_bar',
            config: {
                feeds: [
                    {
                        title: "New York Times",
                        url: "http://www.nytimes.com/services/xml/rss/nyt/HomePage.xml"
                    }
                ],
                showSourceTitle: true,
                showPublishDate: true
            }
        }
	]

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== 'undefined') {module.exports = config;}
