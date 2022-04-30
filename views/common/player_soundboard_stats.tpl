% rebase("common/base.tpl", title=title)

<h1>Last Week</h1>

<table>
    <tr>
        <th>File</th>
        <th>Times Played</th>
    </tr>
    % for filepath, times_played in last_week_stats:
    <tr>
        <td>{{ filepath }}</td>
        <td>{{ times_played }}</td>
    </tr>
    % end
</table>

<h1>Last Month</h1>

<table>
    <tr>
        <th>File</th>
        <th>Times Played</th>
    </tr>
    % for filepath, times_played in last_month_stats:
    <tr>
        <td>{{ filepath }}</td>
        <td>{{ times_played }}</td>
    </tr>
    % end
</table>

<h1>All Time</h1>

<table>
    <tr>
        <th>File</th>
        <th>Times Played</th>
    </tr>
    % for filepath, times_played in all_time_stats:
    <tr>
        <td>{{ filepath }}</td>
        <td>{{ times_played }}</td>
    </tr>
    % end
</table>

