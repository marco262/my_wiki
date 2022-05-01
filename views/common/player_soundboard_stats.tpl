% rebase("common/base.tpl", title=title)

<h1>Last Week</h1>

<table>
    <tr>
        <th>Times Played</th>
        <th>File list</th>
    </tr>
    % for times_played, file_list in last_week_stats:
    <tr>
        <td>{{ times_played }}</td>
        <td>{{ ", ".join(file_list) }}</td>
    </tr>
    % end
</table>

<h1>Last Month</h1>

<table>
    <tr>
        <th>Times Played</th>
        <th>File list</th>
    </tr>
    % for times_played, file_list in last_month_stats:
    <tr>
        <td>{{ times_played }}</td>
        <td>{{ ", ".join(file_list) }}</td>
    </tr>
    % end
</table>

<h1>All Time</h1>

<table>
    <tr>
        <th>Times Played</th>
        <th>File list</th>
    </tr>
    % for times_played, file_list in all_time_stats:
    <tr>
        <td>{{ times_played }}</td>
        <td>{{ ", ".join(file_list) }}</td>
    </tr>
    % end
</table>

