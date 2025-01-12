using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Formatters;
using Microsoft.AspNetCore.Mvc.ModelBinding;
using Microsoft.AspNetCore.Mvc.ModelBinding.Binders;
using Microsoft.AspNetCore.Routing;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;
using Datadog.Trace.AppSec;

namespace weblog
{
    [ApiController]
    [Route("tag_value")]
    public class TagValueController : Controller
    {

        private void DoHeaders()
        {
            const string contentLangHeader = "content-language";

            string contentLang = HttpContext.Request.Query[contentLangHeader].ToString();

            if (!string.IsNullOrWhiteSpace(contentLang))
            {
                HttpContext.Response.Headers.Add(contentLangHeader, contentLang);
            }
        }

        [HttpPost("{tag}/{status}")]
        [Consumes("application/x-www-form-urlencoded")]
        public IActionResult IndexForm(string tag, string status, [FromForm] Model model)
        {
            DoHeaders();

            if (tag != null)
            {
                var details = new Dictionary<string, string>()
                {
                    { "value", tag }
                };
                EventTrackingSdk.TrackCustomEvent("system_tests_appsec_event", details);

                var statusCode = int.Parse(status);
                HttpContext.Response.StatusCode = statusCode;

                return Content($"Value tagged");
            }

            return Content("Hello, World!\\n");

        }

        [HttpGet("{tag}/{status}")]
        public IActionResult IndexForm(string tag, string status)
        {
            DoHeaders();

            if (tag != null)
            {
                var details = new Dictionary<string, string>()
                {
                    { "value", tag }
                };
                EventTrackingSdk.TrackCustomEvent("system_tests_appsec_event", details);

                var statusCode = int.Parse(status);
                HttpContext.Response.StatusCode = statusCode;

                return Content($"Value tagged");
            }

            return Content("Hello, World!\\n");

        }
    }
}
